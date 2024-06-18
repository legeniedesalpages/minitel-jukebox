__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import inject
from minitel.Minitel import Minitel

from vue.commun.Affichable import Affichable


class EcranFinVue(Affichable):

    @inject.autoparams()
    def __init__(self, minitel: Minitel):
        self.__minitel = minitel

    def afficher(self):
        self.__minitel.curseur(False)
        self.__minitel.efface('vraimenttout')
        self.__minitel.position(18, 10)
        self.__minitel.taille(largeur=2, hauteur=2)
        self.__minitel.couleur(caractere='blanc')
        self.__minitel.envoyer('Bye')
        self.__minitel.sortie.join()

    def fermer(self):
        pass
