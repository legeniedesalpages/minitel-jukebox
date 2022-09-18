__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import inject

from modele.composant.AudioModele import AudioModele


class AudioComposantControleur:

    @inject.autoparams()
    def __init__(self, audio_modele: AudioModele):
        self.__audio_modele = audio_modele

    def action_augmenter_volume(self):
        self.__audio_modele.augmenter_volume()

    def action_diminuer_volume(self):
        self.__audio_modele.diminuer_volume()
