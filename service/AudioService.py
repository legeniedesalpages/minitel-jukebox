__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import alsaaudio


class AudioService:
    __PERIPHERIQUE_SORTIE_MASTER = "Master"
    __INCREMENT_VOLUME = 5
    __MAX_VOLUME = 100
    __MIN_VOLUME = 0

    def __init__(self, volume_demarrage):
        logging.info("Initalisation audio:")
        logging.info(f" - Mixeur du périphérique de sortie: {AudioService.__PERIPHERIQUE_SORTIE_MASTER}")
        logging.debug(f" - Cartes de sortie audio connus: {alsaaudio.cards()}")
        logging.debug(f" - Mixers de sortie audio connus: {alsaaudio.mixers()}")

        self.mixer = alsaaudio.Mixer(AudioService.__PERIPHERIQUE_SORTIE_MASTER)

        logging.debug(f"Volume au démarrage avant modification (gauche/droite): {self.mixer.getvolume()}")
        self.mixer.setvolume(volume_demarrage)
        logging.debug(f"Volume configuré: {volume_demarrage}")

        self.volume_actuel = volume_demarrage

    def volume_plus(self):
        nouveau_volume = self.volume_actuel + AudioService.__INCREMENT_VOLUME
        if nouveau_volume <= 100:
            self.mixer.setvolume(nouveau_volume)
            logging.info(f"Augmentation du volume: {nouveau_volume}")
            self.volume_actuel = nouveau_volume
        else:
            logging.debug(f"Volume déjà au maximum")
        return self.volume_actuel

    def volume_moins(self):
        nouveau_volume = self.volume_actuel - AudioService.__INCREMENT_VOLUME
        if nouveau_volume >= 0:
            self.mixer.setvolume(nouveau_volume)
            logging.info(f"Diminution du volume: {nouveau_volume}")
            self.volume_actuel = nouveau_volume
        else:
            logging.debug(f"Volume déjà au minimum")
        return self.volume_actuel
