__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import alsaaudio


class AudioService:
    __PERIPHERIQUE_SORTIE_MASTER = "Master"

    def __init__(self, volume_demarrage=None):
        logging.info("Initalisation audio:")
        logging.info(f" - Mixeur du périphérique de sortie: {AudioService.__PERIPHERIQUE_SORTIE_MASTER}")
        logging.debug(f" - Cartes de sortie audio connus: {alsaaudio.cards()}")
        logging.debug(f" - Mixers de sortie audio connus: {alsaaudio.mixers()}")

        self.__mixer = alsaaudio.Mixer(AudioService.__PERIPHERIQUE_SORTIE_MASTER)

        logging.debug(f"Volume au démarrage avant modification (gauche/droite): {self.__mixer.getvolume()}")
        if volume_demarrage is not None:
            self.__mixer.setvolume(volume_demarrage)
            logging.debug(f"Volume configuré: {volume_demarrage}")

        logging.debug(f"Volume au démarrage après modification (gauche/droite): {self.__mixer.getvolume()}")

    def definir_volume(self, nouveau_volume):
        self.__mixer.setvolume(nouveau_volume)

    def obtenir_volume(self):
        return self.__mixer.getvolume()[0]
