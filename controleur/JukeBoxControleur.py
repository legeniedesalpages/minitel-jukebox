__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject

from modele.AudioModele import AudioModele


class JukeBoxControleur:

    def __init__(self, audio_modele: AudioModele):
        logging.debug("Initialisation UI Contrôleur")
        self.__audio_modele = audio_modele

    def action_augmenter_volume(self):
        logging.debug("Augmenter le volume")
        self.__audio_modele.augmenter_volume()

    def action_diminuer_volume(self):
        logging.debug("Diminuer le volume")
        self.__audio_modele.diminuer_volume()
