__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from enum import Enum

from minitel.Sequence import Sequence

TOUCHE_ECHAP = Sequence(27)
TOUCHE_SHIFT_HAUT = Sequence([27, 91, 77])
TOUCHE_SHIFT_BAS = Sequence([27, 91, 76])


class CaracteresMinitel(Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, dessin, caractere):
        self.dessin = dessin
        self.caractere = caractere

    SABLIER_0 = """
        00000000
        00000000
        00000000
        00000000
        00000000
        01100000
        01100000
        01000000
        00111000
        00000000
    """, "0"

    SABLIER_1 = """
        00000000
        00000000
        01100000
        01100000
        01000000
        01000000
        01000000
        01000000
        00000000
        00000000
    """, "1"

    SABLIER_2 = """
        00000000
        00111000
        01011000
        01000000
        01000000
        00000000
        00000000
        00000000
        00000000
        00000000
    """, "2"

    SABLIER_3 = """
        00000000
        00011100
        00000010
        00000110
        00000110
        00000000
        00000000
        00000000
        00000000
        00000000
    """, "3"

    SABLIER_4 = """
        00000000
        00000000
        00000010
        00000010
        00000010
        00000010
        00000110
        00000110
        00000000
        00000000
    """, "4"

    SABLIER_5 = """
        00000000
        00000000
        00000000
        00000000
        00000000
        00000010
        00000010
        00011010
        00011100
        00000000
    """, "5"

    SEPARATEUR = """
        00000000
        00000000
        00000000
        00000000
        01000100
        00000000
        00000000
        00000000
        00000000
        00000000
    """, "-"

    BARRE_HAUT_VIDE = """
        01111111
        01000001
        01000001
        01001001
        01011101
        01001001
        01000001
        01000001
        01000001
        01000001
    """, "a"

    BARRE_MILIEU_VIDE = """
            01000001
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

    BARRE_BAS_VIDE = """
            01000001
            01000001
            01000001
            01000001
            01000001
            01011101
            01000001
            01000001
            01000001
            01111111
    """, "c"

    BARRE_HAUT_PLEIN = """
            01111111
            01000001
            01011101
            01010101
            01000001
            01010101
            01011101
            01011101
            01011101
            01011101
    """, "d"

    BARRE_MILIEU_PLEIN = """
            01011101
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

    BARRE_BAS_PLEIN = """
            01011101
            01011101
            01011101
            01011101
            01000001
            01011101
            01011101
            01011101
            01000001
            01111111
    """, "f"

    BLUETOOTH_ON = """
            00000000
            00011000
            10010100
            01010010
            00110100
            00111000
            01010100
            10010010
            00010100
            00011000
    """, "B"

    BLUETOOTH_OFF = """
            00000000
            00011000
            10010100
            01010010
            00100100
            00010000
            01001000
            10010100
            00010010
            00011001
    """, "O"

    WIFI_OFF = """
        00000000
        10001000
        01000100
        00100100
        00010010
        10001010
        00010100
        00100010
        00000101
        00001000
    """, "w"

    WIFI_ON = """
        00000000
        00001000
        00000100
        00100100
        00010010
        10010010
        00010010
        00100100
        00000100
        00001000
    """, "W"
