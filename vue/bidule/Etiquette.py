__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from enum import Enum, auto

import math
from minitel.ui.UI import UI


class Alignement(Enum):
    GAUCHE = auto(),
    DROITE = auto(),
    CENTRE = auto(),
    AUCUN = auto(),


class Etiquette(UI):

    def __init__(self, minitel, posx, posy, valeur: str, couleur_texte=None, alignement=Alignement.AUCUN):
        len_valeur_brut = len(valeur.replace("^", ""))
        if alignement is Alignement.AUCUN:
            x = posx
        elif alignement is Alignement.DROITE:
            x = 1
        elif alignement is Alignement.GAUCHE:
            x = 41 - len_valeur_brut
        else:
            x = math.ceil((41 - len_valeur_brut) / 2)

        UI.__init__(self, minitel, x, posy, len_valeur_brut, 1, couleur_texte)

        self.__texte = valeur

        if couleur_texte is None:
            self.__couleur_texte = "blanc"
        else:
            self.__couleur_texte = couleur_texte

    @classmethod
    def aligne(cls, minitel, alignement: Alignement, posy, valeur, couleur_texte=None):
        return cls(minitel, 0, posy, valeur, couleur_texte, alignement)

    def gere_touche(self, sequence):
        return False

    def affiche(self):
        self.minitel.position(self.posx, self.posy)
        self.minitel.couleur(self.__couleur_texte)
        flip_flop = False
        for mot in self.__texte.split("^"):
            self.minitel.effet(inversion=flip_flop)
            self.minitel.envoyer(mot)
            flip_flop = not flip_flop
