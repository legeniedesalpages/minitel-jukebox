__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import logging
from typing import Optional

from minitel.Sequence import Sequence

from controleur.PeutGererTouche import PeutGererTouche
from service.minitel.MinitelConstante import TOUCHE_SHIFT_HAUT, TOUCHE_SHIFT_BAS


class AudioControleur(PeutGererTouche):
    def gere_touche(self, touche: Sequence) -> Optional[bool]:
        if touche.egale(TOUCHE_SHIFT_HAUT):
            logging.info("Volume +")
            return False
        elif touche.egale(TOUCHE_SHIFT_BAS):
            logging.info("Volume -")
            return False
        return None
