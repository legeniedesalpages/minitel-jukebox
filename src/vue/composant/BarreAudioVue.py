__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from threading import Timer

import inject
from minitel.Minitel import Minitel
from pyobservable import Observable

from controleur.composant.AudioControleur import AudioControleur
from modele.audio.AudioModele import AudioModele
from service.minitel.MinitelConfiguration import CaracteresMinitel
from service.minitel.MinitelExtension import MinitelExtension


class BarreAudioVue:
    __DELAI_EFFACEMENT_EN_SECONDES = 3
    __COULEUR = "blanc"
    __POS_X = 40
    __POS_Y = 2

    __audio_composant_controleur = inject.attr(AudioControleur)
    __audio_modele = inject.attr(AudioModele)
    __notificateur_evenement = inject.attr(Observable)
    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)

    def __init__(self, callback_positionnement_curseur):
        logging.debug("Création du composant visuel Audio")
        self.__thread_effaceur = None
        self.__callback_positionnement_curseur = callback_positionnement_curseur
        self.__notificateur_evenement.bind(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, self._dessin)
        self.__visible = False

    def fermer(self):
        logging.debug("Destruction du composant visuel Audio")
        self.__notificateur_evenement.unbind(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, self._dessin)
        if self.__thread_effaceur is not None and self.__thread_effaceur.is_alive():
            self.__thread_effaceur.cancel()

    def _dessin(self, type_changement):

        if self.__visible is True and type_changement == AudioModele.VOLUME_STAGNE:
            logging.debug("On ne redessine rien")

        else:
            volume = self.__audio_modele.obtenir_volume()
            logging.debug(f"Dessine le volume: {type_changement} => {volume}")

            position = int((AudioModele.MAX_VOLUME - volume) / 5)
            if type_changement == AudioModele.VOLUME_MONTE:
                ancienne_position = int((AudioModele.MAX_VOLUME - volume) / 5) + 1
            elif type_changement == AudioModele.VOLUME_DESCEND:
                ancienne_position = int((AudioModele.MAX_VOLUME - volume) / 5) - 1
            else:
                ancienne_position = position

            self.__minitel.curseur(False)
            self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()

            logging.debug(f"{ancienne_position} => {position}")

            if ancienne_position == 0 or position == 0 or self.__visible is False:
                self.__minitel_extension.position_couleur(BarreAudioVue.__POS_X, BarreAudioVue.__POS_Y, BarreAudioVue.__COULEUR)
                if volume == AudioModele.MAX_VOLUME:
                    logging.info("Volume max")
                    self.__minitel.envoyer(CaracteresMinitel.BARRE_HAUT_PLEIN.caractere)
                else:
                    self.__minitel.envoyer(CaracteresMinitel.BARRE_HAUT_VIDE.caractere)

            if self.__visible is False:
                for i in range(1, 19):
                    self.__dessin_barre_milieu(i, position)
            else:
                self.__dessin_barre_milieu(position, position)
                self.__dessin_barre_milieu(ancienne_position, position)

            if ancienne_position == 20 or position == 20 or self.__visible is False:
                self.__minitel_extension.position_couleur(BarreAudioVue.__POS_X, BarreAudioVue.__POS_Y + 19, BarreAudioVue.__COULEUR)
                if volume == AudioModele.MIN_VOLUME:
                    self.__minitel.envoyer(CaracteresMinitel.BARRE_BAS_VIDE.caractere)
                else:
                    self.__minitel.envoyer(CaracteresMinitel.BARRE_BAS_PLEIN.caractere)

            self.__minitel_extension.revenir_jeu_caractere_standard()
            self.__callback_positionnement_curseur()
            self.__visible = True

        self.__demarrer_effacement_programme()

    def _efface(self):
        logging.debug("efface")
        self.__minitel.curseur(False)
        for i in range(0, 20):
            self.__minitel.position(40, BarreAudioVue.__POS_Y + i)
            self.__minitel.envoyer(" ")
        self.__callback_positionnement_curseur()
        self.__visible = False

    def __dessin_barre_milieu(self, i, int_volume):
        if 1 <= i < 19:
            self.__minitel_extension.position_couleur(BarreAudioVue.__POS_X, BarreAudioVue.__POS_Y + i, BarreAudioVue.__COULEUR)
            if i < int_volume:
                self.__minitel.envoyer(CaracteresMinitel.BARRE_MILIEU_VIDE.caractere)
            else:
                self.__minitel.envoyer(CaracteresMinitel.BARRE_MILIEU_PLEIN.caractere)

    def __demarrer_effacement_programme(self):
        if self.__thread_effaceur is not None and self.__thread_effaceur.is_alive():
            logging.debug("Un précédent effaceur était en cours, on l'annule")
            self.__thread_effaceur.cancel()

        logging.debug("Démarre le timer d'effacement")
        self.__thread_effaceur = Timer(BarreAudioVue.__DELAI_EFFACEMENT_EN_SECONDES, self._efface)
        self.__thread_effaceur.start()
