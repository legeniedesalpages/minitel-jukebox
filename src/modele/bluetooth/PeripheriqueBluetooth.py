__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2023-11-20"
__version__ = "1.0.0"

from enum import Enum, auto


class PeripheriqueBluetooth:
    # noinspection PyArgumentList
    class TypeStatut(Enum):
        INCONNU = auto()
        COUPLE = auto()
        CONNECTE = auto()

    def __init__(self, nom, adresse_mac, statut: TypeStatut):
        self.nom = nom
        self.adresse_mac = adresse_mac
        self.statut = statut

    def __str__(self):
        return f"{self.nom} ({self.adresse_mac}) : {self.statut}"
