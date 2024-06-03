__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
import math
from enum import Enum, auto

import inject
from minitel.Minitel import Minitel


# noinspection PyArgumentList
class Alignement(Enum):
    GAUCHE = auto(),
    DROITE = auto(),
    CENTRE = auto(),
    AUCUN = auto(),


class Etiquette:
    __minitel = inject.attr(Minitel)

    def __init__(self, posx, posy, texte: str, couleur_texte=None, alignement=Alignement.AUCUN):
        logging.debug(f"Initialisation d'une étiquette {texte}")
        self.__posy = posy
        len_valeur_brut = len(texte.replace("^", ""))
        if alignement is Alignement.AUCUN:
            self.__posx = posx
        elif alignement is Alignement.GAUCHE:
            self.__posx = 1
        elif alignement is Alignement.DROITE:
            self.__posx = 40 - len_valeur_brut
        else:
            self.__posx = math.ceil((40 - len_valeur_brut) / 2)  # Alignement.CENTRE

        self.__texte = texte

        if couleur_texte is None:
            self.__couleur_texte = "blanc"
        else:
            self.__couleur_texte = couleur_texte

    def affiche(self):
        self.__minitel.position(self.__posx, self.__posy)
        self.__minitel.couleur(self.__couleur_texte)
        flip_flop = False
        for mot in self.__texte.split("^"):
            self.__minitel.effet(inversion=flip_flop)
            self.__minitel.envoyer(mot)
            flip_flop = not flip_flop

    @classmethod
    def gauche(cls, posy, texte, couleur_texte="blanc"):
        return cls(0, posy, texte, couleur_texte, Alignement.GAUCHE).affiche()

    @classmethod
    def droite(cls, posy, texte, couleur_texte="blanc"):
        return cls(0, posy, texte, couleur_texte, Alignement.DROITE).affiche()

    @classmethod
    def centre(cls, posy, texte, couleur_texte="blanc"):
        return cls(0, posy, texte, couleur_texte, Alignement.CENTRE).affiche()
