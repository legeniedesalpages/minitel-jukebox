__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
from pyobservable import Observable

from service.AudioService import AudioService


class AudioModele:
    EVENEMENT_CHANGEMENT_VOLUME = "ChangementVolume"

    __INCREMENT_VOLUME = 5
    __MAX_VOLUME = 100
    __MIN_VOLUME = 0

    @inject.autoparams()
    def __init__(self, audio_service: AudioService, notificateur_evenement: Observable):
        self.__volume = 50
        self.__mute = False
        self.__notificateur_evenement = notificateur_evenement
        self.__audio_service = audio_service

    def augmenter_volume(self):
        nouveau_volume = self.__volume + AudioModele.__INCREMENT_VOLUME
        if nouveau_volume <= 100:
            logging.info(f"Augmentation du volume: {nouveau_volume}")
            self.__volume = nouveau_volume
            self.__audio_service.definir_volume(nouveau_volume)
            self.__notificateur_evenement.notify(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, nouveau_volume)
        else:
            logging.debug("Volume déjà au maximum")
        return self.__volume

    def diminuer_volume(self):
        nouveau_volume = self.__volume - AudioModele.__INCREMENT_VOLUME
        if nouveau_volume >= 0:
            logging.info(f"Diminution du volume: {nouveau_volume}")
            self.__volume = nouveau_volume
            self.__notificateur_evenement.notify(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, nouveau_volume)
        else:
            logging.debug("Volume déjà au minimum")
        return self.__volume
