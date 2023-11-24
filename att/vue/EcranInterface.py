__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from minitel.constantes import GUIDE

from modele.JukeBoxModele import EvenementSortieEcran


class EcranInterface:

    def afficher(self):
        pass

    def fermer(self):
        pass

    def gerer_touche(self, sequence) -> EvenementSortieEcran:
        if sequence.egale(GUIDE):
            return EvenementSortieEcran.CONFIGURATION_BLUETOOTH
