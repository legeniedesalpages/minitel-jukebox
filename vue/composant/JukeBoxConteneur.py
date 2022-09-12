__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from _queue import Empty
from minitel.Minitel import Minitel
from minitel.ui.Conteneur import Conteneur


class JukeBoxConteneur(Conteneur):
    __TOUCHE_ENVOI = [19, 65]
    __TOUCHE_ENTREE = [13]

    def __init__(self, minitel: Minitel, callback_touche_envoi, callback_touche_entree):
        super().__init__(minitel, 1, 1, 40, 23, "blanc", "noir")
        self.__callback_touche_envoi = callback_touche_envoi
        self.__callback_touche_entree = callback_touche_entree
        self.__continuer = True

    def gere_touche(self, sequence):

        if self.element_actif.gere_touche(sequence):
            return True

        for element in self.elements:
            if self.element_actif != element:
                if element.gere_touche(sequence):
                    return True

        touche = sequence.valeurs
        if touche == JukeBoxConteneur.__TOUCHE_ENVOI:
            self.__callback_touche_envoi()
            self.__continuer = False
            return True

        if touche == JukeBoxConteneur.__TOUCHE_ENTREE:
            self.__callback_touche_entree()
            return True

        return False

    def executer(self):
        self.__continuer = True
        while self.__continuer:
            try:
                r = self.minitel.recevoir_sequence(attente=None)
                self.gere_touche(r)
            except Empty:
                pass
