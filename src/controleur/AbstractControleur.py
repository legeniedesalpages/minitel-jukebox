__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from typing import List, Optional

from minitel.Minitel import Minitel


class AbstractControleur:
    __vue: Optional

    def __init__(self, minitel: Minitel, modeles: List):
        self.__minitel = minitel
        logging.info("Controleur créé")

    def enregistrer_vue(self, vue):
        self.__vue = vue
