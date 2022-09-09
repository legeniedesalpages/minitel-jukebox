__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from threading import Timer

import inject
from minitel.Minitel import Minitel
from minitel.ui.UI import UI
from pyobservable import Observable

from modele.composant.AudioModele import AudioModele


class AudioComposant(UI):
    __TOUCHE_HAUT = [27, 91, 65]
    __TOUCHE_BAS = [27, 91, 66]

    __COLONNE = 40
    _LIGNE = 1

    __DELAI_SECONDE_EFFACEMENT = 4

    @inject.autoparams()
    def __init__(self, minitel: Minitel, audio_modele: AudioModele, notificateur_evenement: Observable):
        super().__init__(minitel, 1, 1, 1, 1, "noir")
        self.__minitel = minitel
        self.__audio_modele = audio_modele
        self.__effaceur = None
        notificateur_evenement.bind(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, self.dessin)

    def __efface(self):
        self.__minitel.curseur(False)
        for i in range(0, 20):
            self.__minitel.position(AudioComposant.__COLONNE, i + AudioComposant._LIGNE)
            self.__minitel.couleur("noir", "noir")
            self.__minitel.envoyer(" ")

    def dessin(self, volume):
        self.__minitel.curseur(False)
        self.__minitel.effet(inversion=True)
        int_volume = int((AudioModele.MAX_VOLUME - volume) / 5)
        for i in range(0, int_volume):
            self.__minitel.position(AudioComposant.__COLONNE, i + AudioComposant._LIGNE)
            self.__minitel.couleur("noir", "bleu")
            self.__minitel.envoyer(" ")
        for i in range(int_volume, 20):
            self.__minitel.position(AudioComposant.__COLONNE, i + AudioComposant._LIGNE)
            self.__minitel.couleur("noir", "blanc")
            self.__minitel.envoyer(" ")
        self.__minitel.effet(inversion=False)

        self.__demarrer_effacement_programme()

    def __demarrer_effacement_programme(self):
        if self.__effaceur is not None and self.__effaceur.is_alive():
            self.__effaceur.cancel()
        self.__effaceur = Timer(AudioComposant.__DELAI_SECONDE_EFFACEMENT, self.__efface)
        self.__effaceur.start()

    def gere_touche(self, sequence):
        touche = sequence.valeurs
        logging.debug(f"Touche appuyée: {touche}")

        if touche == AudioComposant.__TOUCHE_HAUT:
            self.__audio_modele.augmenter_volume()
            return True

        if touche == AudioComposant.__TOUCHE_BAS:
            self.__audio_modele.diminuer_volume()
            return True

        return False
