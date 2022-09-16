__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from modele.JukeBoxModele import EvenementSortieEcran


class EcranInterface:

    def afficher(self) -> EvenementSortieEcran:
        pass

    def fermer(self):
        pass
