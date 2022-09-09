__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from minitel.ui.Label import Label


class MenuFixeComposant(Label):

    def __init__(self, minitel, posy, texte, menu, couleur='blanc'):
        super().__init__(minitel, 1, posy, texte, couleur)
        self.__minitel = minitel
        self.__menu = menu

    def affiche(self):
        depart = 41 - (len(self.valeur) + 3 + len(self.__menu))
        self.minitel.position(depart, self.posy)
        self.minitel.couleur(caractere=self.couleur)
        self.minitel.effet(inversion=False)
        self.minitel.envoyer(self.valeur)

        self.minitel.envoyer(" → ")

        self.minitel.couleur(caractere=self.couleur)
        self.minitel.effet(inversion=True)
        self.minitel.envoyer(self.__menu)
