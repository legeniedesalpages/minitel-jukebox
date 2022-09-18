__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from threading import Timer

import inject
from minitel.Minitel import Minitel
from minitel.constantes import ESC
from pyobservable import Observable

from configuration.MinitelConfiguration import CaracteresMinitel
from controleur.composant.AudioComposantControleur import AudioComposantControleur
from modele.composant.AudioModele import AudioModele
from service.MinitelConstante import TOUCHE_FLECHE_HAUT, TOUCHE_FLECHE_BAS
from vue.composant.InterfaceComposantVue import InterfaceComposantVue


class AudioComposantVue(InterfaceComposantVue):
    __COLONNE_AFFICHAGE_COMPOSANT = 40
    _LIGNE_AFFICHAGE_COMPOSANT = 2
    __DELAI_EFFACEMENT_EN_SECONDES = 2

    @inject.autoparams()
    def __init__(self, minitel: Minitel, audio_composant_controleur: AudioComposantControleur,
                 audio_modele: AudioModele, notificateur_evenement: Observable):
        self.__minitel = minitel
        self.__audio_composant_controleur = audio_composant_controleur
        self.__audio_modele = audio_modele
        self.__effaceur = None
        self.__notificateur_evenement = notificateur_evenement

    def afficher(self):
        logging.debug("Affichage du composant de volume : on affiche rien au démarrage")
        self.__notificateur_evenement.bind(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, self.dessin)

    def fermer(self):
        self.__notificateur_evenement.unbind(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, self.dessin)

    def dessin(self, volume):
        logging.debug(f"volume:{volume}")
        int_volume = int((AudioModele.MAX_VOLUME - volume) / 5)
        col = AudioComposantVue.__COLONNE_AFFICHAGE_COMPOSANT
        ligne = AudioComposantVue._LIGNE_AFFICHAGE_COMPOSANT

        self.__minitel.curseur(False)
        self.__minitel.couleur("bleu", "noir")
        self.__minitel.envoyer([ESC, 0x28, 0x20, 0x42])

        self.__minitel.position(col, ligne)
        if volume == AudioModele.MAX_VOLUME:
            self.__minitel.envoyer(CaracteresMinitel.BARRE_HAUT_PLEIN.caractere)
        else:
            self.__minitel.envoyer(CaracteresMinitel.BARRE_HAUT_VIDE.caractere)
            for i in range(int_volume, 19):
                self.__minitel.position(col, i + ligne)
                self.__minitel.envoyer(CaracteresMinitel.BARRE_MILIEU_PLEIN.caractere)

        for i in range(1, int_volume):
            self.__minitel.position(col, i + ligne)
            self.__minitel.envoyer(CaracteresMinitel.BARRE_MILIEU_VIDE.caractere)

        self.__minitel.position(col, ligne + 19)
        if volume == AudioModele.MIN_VOLUME:
            self.__minitel.envoyer(CaracteresMinitel.BARRE_BAS_VIDE.caractere)
        else:
            self.__minitel.envoyer(CaracteresMinitel.BARRE_BAS_PLEIN.caractere)

        # TODO : repositionnement du curseur

        self.__minitel.envoyer([ESC, 0x28, 0x40])
        self.__demarrer_effacement_programme()

    def __demarrer_effacement_programme(self):
        if self.__effaceur is not None and self.__effaceur.is_alive():
            self.__effaceur.cancel()
        self.__effaceur = Timer(AudioComposantVue.__DELAI_EFFACEMENT_EN_SECONDES, self.__efface)
        self.__effaceur.start()

    def __efface(self):
        self.__minitel.curseur(False)
        for i in range(0, 20):
            self.__minitel.position(AudioComposantVue.__COLONNE_AFFICHAGE_COMPOSANT,
                                    i + AudioComposantVue._LIGNE_AFFICHAGE_COMPOSANT)
            self.__minitel.couleur("noir", "noir")
            self.__minitel.envoyer(" ")

    def gere_touche(self, touche) -> bool:

        if touche == TOUCHE_FLECHE_HAUT:
            self.__audio_composant_controleur.action_augmenter_volume()
            return True

        if touche == TOUCHE_FLECHE_BAS:
            self.__audio_composant_controleur.action_diminuer_volume()
            return True

        return False
