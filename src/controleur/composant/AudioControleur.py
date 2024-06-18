__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import logging
from typing import Optional

from minitel.Sequence import Sequence

from controleur.commun.PeutGererTouche import PeutGererTouche
from modele.audio.AudioModele import AudioModele
from service.minitel.MinitelConstante import TOUCHE_SHIFT_HAUT, TOUCHE_SHIFT_BAS


class AudioControleur(PeutGererTouche):

    def __init__(self, audio_modele: AudioModele):
        self.__audio_modele = audio_modele

    def gere_touche(self, touche: Sequence) -> Optional[bool]:

        if touche.egale(TOUCHE_SHIFT_HAUT):
            logging.info("Volume +")
            self.__audio_modele.augmenter_volume()
            return False

        elif touche.egale(TOUCHE_SHIFT_BAS):
            self.__audio_modele.diminuer_volume()
            logging.info("Volume -")
            return False

        return None
