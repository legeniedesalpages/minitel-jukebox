__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from typing import List

from minitel.Minitel import Minitel

from controleur.AbstractControleur import AbstractControleur
from service.minitel.MinitelExtension import MinitelExtension


class AbstractVue:

    def __init__(self, minitel: Minitel, minitel_extension: MinitelExtension, controleur: AbstractControleur,
                 modeles: List):
        self.__minitel = minitel
        self.__minitel_extension = minitel_extension
