__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject

from modele.AudioModele import AudioModele
from modele.LecteurModele import LecteurModele


class ComposantControleur:

    @inject.autoparams()
    def __init__(self, audio_modele: AudioModele, lecteur_modele: LecteurModele):
        logging.debug("Initialisation UI Contrôleur")
        self.__audio_modele = audio_modele
        self.__lecteur_modele = lecteur_modele

    def action_augmenter_volume(self):
        logging.debug("Augmenter le volume")
        self.__audio_modele.augmenter_volume()

    def action_diminuer_volume(self):
        logging.debug("Diminuer le volume")
        self.__audio_modele.diminuer_volume()

    def action_jouer_chanson(self, titre_chanson):
        logging.debug(f"Jouer chanson: {titre_chanson}")
        self.__lecteur_modele.jouer_chanson(titre_chanson)

    def action_pause_ou_reprendre(self):
        logging.debug("Mise en pause ou reprise")
        self.__lecteur_modele.pause_ou_reprendre()
