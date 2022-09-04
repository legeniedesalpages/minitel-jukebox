__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from minitel.Minitel import Minitel
from minitel.ui.Conteneur import Conteneur


class JukeBoxConteneur(Conteneur):

    def __init__(self, minitel: Minitel):
        super().__init__(minitel, 1, 1, 40, 23, "blanc", "noir")

    def gere_touche(self, sequence):

        touche_geree = self.element_actif.gere_touche(sequence)

        if not touche_geree:
            for element in self.elements:
                if self.element_actif != element:
                    element.gere_touche(sequence)
