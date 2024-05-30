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
from minitel.ui.UI import UI


class Alignement(Enum):
    GAUCHE = auto(),
    DROITE = auto(),
    CENTRE = auto(),
    AUCUN = auto(),


class Etiquette(UI):
    __minitel = inject.attr(Minitel)

    def __init__(self, posx, posy, valeur: str, couleur_texte=None, alignement=Alignement.AUCUN):
        logging.debug(f"Initialisation d'une étiquette {valeur}")
        len_valeur_brut = len(valeur.replace("^", ""))
        if alignement is Alignement.AUCUN:
            x = posx
        elif alignement is Alignement.GAUCHE:
            x = 1
        elif alignement is Alignement.DROITE:
            x = 41 - len_valeur_brut
        else:
            x = math.ceil((41 - len_valeur_brut) / 2)

        UI.__init__(self, self.__minitel, x, posy, len_valeur_brut, 1, couleur_texte)

        self.__texte = valeur

        if couleur_texte is None:
            self.__couleur_texte = "blanc"
        else:
            self.__couleur_texte = couleur_texte

    @classmethod
    def aligne(cls, alignement: Alignement, posy, valeur, couleur_texte=None):
        return cls(0, posy, valeur, couleur_texte, alignement)

    def gere_touche(self, sequence):
        return False

    def affiche(self):
        self.__minitel.position(self.posx, self.posy)
        self.__minitel.couleur(self.__couleur_texte)
        flip_flop = False
        for mot in self.__texte.split("^"):
            if len(mot) > 0 and mot[0] == '_':
                mot = mot[1:]
                clignotant = True
            else:
                clignotant = False
            self.__minitel.effet(inversion=flip_flop, clignotement=clignotant)
            self.__minitel.envoyer(mot)
            flip_flop = not flip_flop
