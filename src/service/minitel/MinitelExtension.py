__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from minitel.Minitel import Minitel
from minitel.constantes import ESC


class MinitelExtension:

    @staticmethod
    def demarrer_affichage_jeu_caractere_redefinit(minitel: Minitel):
        minitel.envoyer([ESC, 0x28, 0x20, 0x42])

    @staticmethod
    def revenir_jeu_caractere_standard(minitel: Minitel):
        minitel.envoyer([ESC, 0x28, 0x40])

    @staticmethod
    def position_couleur(minitel: Minitel, posx, posy, couleur):
        minitel.position(posx, posy)
        minitel.couleur(couleur)

    @staticmethod
    def separateur(minitel: Minitel, posy, couleur):
        minitel.position(1, posy)
        minitel.couleur(couleur)
        minitel.repeter(0x60, 39)
