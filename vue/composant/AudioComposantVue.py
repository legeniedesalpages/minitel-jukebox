__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from threading import Timer

import inject
from minitel.Minitel import Minitel
from minitel.constantes import HAUT, BAS
from minitel.ui.UI import UI
from pyobservable import Observable

from controleur.composant.AudioComposantControleur import AudioComposantControleur
from modele.composant.AudioModele import AudioModele
from service.minitel.MinitelConfiguration import CaracteresMinitel
from service.minitel.MinitelExtension import MinitelExtension


class AudioComposantVue(UI):
    __DELAI_EFFACEMENT_EN_SECONDES = 3

    __minitel_extension = inject.attr(MinitelExtension)
    __audio_composant_controleur = inject.attr(AudioComposantControleur)
    __audio_modele = inject.attr(AudioModele)
    __notificateur_evenement = inject.attr(Observable)

    def __init__(self, minitel: Minitel, posx, posy, callback_positionnement_curseur):
        logging.debug("Création du composant visuel Audio")
        super().__init__(
            minitel=minitel,
            posx=posx,
            posy=posy,
            largeur=1,
            hauteur=20,
            couleur=None
        )
        self.__thread_effaceur = None
        self.__callback_positionnement_curseur = callback_positionnement_curseur
        self.__notificateur_evenement.bind(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, self._dessin)
        self.__visible = False

    def fermer(self):
        logging.debug("Destruction du composant visuel Audio")
        self.__notificateur_evenement.unbind(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, self._dessin)
        if self.__thread_effaceur is not None and self.__thread_effaceur.is_alive():
            self.__thread_effaceur.cancel()

    def efface(self):
        self.minitel.curseur(False)
        super().efface()
        self.__callback_positionnement_curseur()
        self.__visible = False

    def gere_touche(self, sequence):

        if sequence.egale(HAUT):
            self.__audio_composant_controleur.action_augmenter_volume()
            return True

        if sequence.egale(BAS):
            self.__audio_composant_controleur.action_diminuer_volume()
            return True

        return False

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

            self.minitel.curseur(False)
            self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()

            if ancienne_position == 0 or position == 0 or self.__visible is False:
                self.__minitel_extension.position_couleur(self.posx, self.posy, self.couleur)
                if volume == AudioModele.MAX_VOLUME:
                    self.minitel.envoyer(CaracteresMinitel.BARRE_HAUT_PLEIN.caractere)
                else:
                    self.minitel.envoyer(CaracteresMinitel.BARRE_HAUT_VIDE.caractere)

            if self.__visible is False:
                for i in range(1, 19):
                    self.__dessin_barre_milieu(i, position)
            else:
                self.__dessin_barre_milieu(position, position)
                self.__dessin_barre_milieu(ancienne_position, position)

            if ancienne_position == 20 or position == 20 or self.__visible is False:
                self.__minitel_extension.position_couleur(self.posx, self.posy + 19, self.couleur)
                if volume == AudioModele.MIN_VOLUME:
                    self.minitel.envoyer(CaracteresMinitel.BARRE_BAS_VIDE.caractere)
                else:
                    self.minitel.envoyer(CaracteresMinitel.BARRE_BAS_PLEIN.caractere)

            self.__minitel_extension.revenir_jeu_caractere_standard()
            self.__callback_positionnement_curseur()
            self.__visible = True

        self.__demarrer_effacement_programme()

    def __dessin_barre_milieu(self, i, int_volume):
        if 1 <= i < 19:
            self.__minitel_extension.position_couleur(self.posx, self.posy + i, self.couleur)
            if i < int_volume:
                self.minitel.envoyer(CaracteresMinitel.BARRE_MILIEU_VIDE.caractere)
            else:
                self.minitel.envoyer(CaracteresMinitel.BARRE_MILIEU_PLEIN.caractere)

    def __demarrer_effacement_programme(self):
        if self.__thread_effaceur is not None and self.__thread_effaceur.is_alive():
            logging.debug("Un précédent effaceur était en cours, on l'annule")
            self.__thread_effaceur.cancel()

        self.__thread_effaceur = Timer(AudioComposantVue.__DELAI_EFFACEMENT_EN_SECONDES, self.efface)
        self.__thread_effaceur.start()
