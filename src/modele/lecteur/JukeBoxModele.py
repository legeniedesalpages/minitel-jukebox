__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from enum import Enum, auto
from typing import Optional


# noinspection PyArgumentList
class Ecran(Enum):
    ECRAN_VISUALISATION = auto(),
    ECRAN_BLUETOOTH = auto(),
    ECRAN_LISTE_LECTURE = auto(),
    ECRAN_RECHERCHE = auto(),
    ECRAN_GUIDE = auto(),
    ECRAN_BIBLIOTHEQUE_SPOTIFY = auto()


class JukeBoxModele:
    EVENEMENT_NOTIFICATION = "evenementNotification"

    ecran_courant: Optional[Ecran]
    ecran_demande: Optional[Ecran]

    def __init__(self):
        self.__est_termine = False
        self.ecran_courant = None
        self.ecran_demande = Ecran.ECRAN_BLUETOOTH

    def switch_ecran(self):
        self.ecran_courant = self.ecran_demande
        self.ecran_demande = None

    def arreter_jukebox(self):
        self.__est_termine = True

    def est_termine(self) -> bool:
        return self.__est_termine
