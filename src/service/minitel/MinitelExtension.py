__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import inject
from minitel.Minitel import Minitel
from minitel.constantes import ESC


class MinitelExtension:
    __minitel = inject.attr(Minitel)

    def demarrer_affichage_jeu_caractere_redefinit(self):
        self.__minitel.envoyer([ESC, 0x28, 0x20, 0x42])

    def revenir_jeu_caractere_standard(self):
        self.__minitel.envoyer([ESC, 0x28, 0x40])

    def position_couleur(self, posx, posy, couleur):
        self.__minitel.position(posx, posy)
        self.__minitel.couleur(couleur)

    def envoyer_ligne(self, posy=None, texte="", couleur="blanc", inversion=False):
        if posy is not None:
            self.position_couleur(1, posy, couleur)
        else:
            self.__minitel.couleur(couleur)

        sequence = texte[:39].ljust(40, " ")
        if inversion:
            self.__minitel.effet(inversion=True)
        self.__minitel.envoyer(sequence)
        self.__minitel.effet(inversion=False)

    def effacer_ligne(self, posy):
        self.__minitel.position(1, posy)
        self.__minitel.repeter(" ", 40)
