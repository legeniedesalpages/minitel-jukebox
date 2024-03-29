__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
from pyobservable import Observable

from service.audio.AudioService import AudioService


class AudioModele:
    EVENEMENT_CHANGEMENT_VOLUME = "EvenementChangementVolume"

    VOLUME_MONTE = "VolumeMonte"
    VOLUME_DESCEND = "VolumeDescend"
    VOLUME_STAGNE = "VolumeStagne"

    __INCREMENT_VOLUME = 5
    MAX_VOLUME = 100
    MIN_VOLUME = 0

    @inject.autoparams()
    def __init__(self, audio_service: AudioService, notificateur_evenement: Observable):
        self.__notificateur_evenement = notificateur_evenement
        self.__audio_service = audio_service
        self.__volume = self.__audio_service.obtenir_volume()

    def augmenter_volume(self):
        nouveau_volume = self.__volume + AudioModele.__INCREMENT_VOLUME
        if nouveau_volume <= AudioModele.MAX_VOLUME:
            logging.info(f"Augmentation du volume: {nouveau_volume}")
            self.__audio_service.definir_volume(nouveau_volume)
            self.__volume = nouveau_volume
            self.__notificateur_evenement.notify(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, AudioModele.VOLUME_MONTE)
        else:
            logging.debug("Volume déjà au maximum")
            self.__notificateur_evenement.notify(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, AudioModele.VOLUME_STAGNE)

        return self.__volume

    def diminuer_volume(self):
        nouveau_volume = self.__volume - AudioModele.__INCREMENT_VOLUME
        if nouveau_volume >= AudioModele.MIN_VOLUME:
            logging.info(f"Diminution du volume: {nouveau_volume}")
            self.__audio_service.definir_volume(nouveau_volume)
            self.__volume = nouveau_volume
            self.__notificateur_evenement.notify(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, AudioModele.VOLUME_DESCEND)
        else:
            logging.debug("Volume déjà au minimum")
            self.__notificateur_evenement.notify(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, AudioModele.VOLUME_STAGNE)

        return self.__volume

    def obtenir_volume(self) -> int:
        return self.__volume
