__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from minitel.Minitel import Minitel
from minitel.constantes import ESC


class MinitelExtension:

    def __init__(self, minitel: Minitel):
        self.__minitel = minitel

    def demarrer_affichage_jeu_caractere_redefinit(self):
        self.__minitel.envoyer([ESC, 0x28, 0x20, 0x42])

    def revenir_jeu_caractere_standard(self):
        self.__minitel.envoyer([ESC, 0x28, 0x40])

    def position_couleur(self, posx, posy, couleur):
        self.__minitel.position(posx, posy)
        self.__minitel.couleur(couleur)

    def separateur(self, posy, couleur):
        self.__minitel.position(1, posy)
        self.__minitel.couleur(couleur)
        self.__minitel.repeter(0x60, 40)
