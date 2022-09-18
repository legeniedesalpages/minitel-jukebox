__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from enum import Enum

from minitel.Minitel import Minitel
from minitel.constantes import PRO1, RESET


def produire_minitel() -> Minitel:
    minitel = Minitel("/dev/ttyUSB0")
    minitel.deviner_vitesse()
    minitel.identifier()
    minitel.definir_vitesse(9600)
    minitel.definir_mode("VIDEOTEX")
    minitel.appeler([PRO1, RESET], 1)
    minitel.configurer_clavier(etendu=True, curseur=False, minuscule=True)
    minitel.echo(False)
    minitel.curseur(False)
    minitel.efface('vraimenttout')

    for car in CaracteresMinitel:
        minitel.redefinir(car.caractere, car.dessin)

    logging.info(f"Création du minitel terminé, vitesse => {minitel.vitesse}")

    return minitel


class CaracteresMinitel(Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, dessin, caractere):
        self.dessin = dessin
        self.caractere = caractere

    BARRE_HAUT_VIDE = """01111111
        01000001
        01000001
        01000001
        01000001
        01000001
        01000001
        01000001
        01000001
        01000001
    """, "a"

    BARRE_MILIEU_VIDE = """01000001
            01000001
            01000001
            01000001
            01000001
            01000001
            01000001
            01000001
            01000001
            01000001
    """, "b"

    BARRE_BAS_VIDE = """01000001
            01000001
            01000001
            01000001
            01000001
            01000001
            01000001
            01000001
            01000001
            01111111
    """, "c"

    BARRE_HAUT_PLEIN = """01111111
            01000001
            01011101
            01011101
            01011101
            01011101
            01011101
            01011101
            01011101
            01011101
    """, "d"

    BARRE_MILIEU_PLEIN = """01011101
            01011101
            01011101
            01011101
            01011101
            01011101
            01011101
            01011101
            01011101
            01011101
    """, "e"

    BARRE_BAS_PLEIN = """01011101
            01011101
            01011101
            01011101
            01011101
            01011101
            01011101
            01011101
            01000001
            01111111
    """, "f"
