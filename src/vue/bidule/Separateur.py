__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-31"
__version__ = "1.0.0"

from enum import Enum, auto

import inject
from minitel.Minitel import Minitel

from service.minitel.MinitelExtension import MinitelExtension


# noinspection PyArgumentList
class Remplissage(Enum):
    PLEIN = auto(),
    MOYEN = auto(),
    LEGER = auto(),


class Separateur:
    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)

    def __init__(self, posy, couleur=None, remplissage=Remplissage.PLEIN):
        self.__minitel_extension.position_couleur(1, posy, couleur)
        if remplissage == Remplissage.PLEIN:
            self.__minitel.repeter(0x60, 39)
        elif remplissage == Remplissage.LEGER:
            self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()
            self.__minitel.repeter("-", 39)
            self.__minitel_extension.revenir_jeu_caractere_standard()

    @classmethod
    def plein(cls, posy, couleur="rouge"):
        return cls(posy, couleur, Remplissage.PLEIN)

    @classmethod
    def leger(cls, posy, couleur="rouge"):
        return cls(posy, couleur, Remplissage.LEGER)
