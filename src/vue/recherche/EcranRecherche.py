__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from minitel.Minitel import Minitel

from controleur.recherche.RechercheControleur import RechercheControleur
from vue.AbstractEcran import AbstractEcran


class EcranRecherche(AbstractEcran):

    def __init__(self, minitel: Minitel, recherche_controleur: RechercheControleur, modeles: dict[str, object]):
        super().__init__(minitel, recherche_controleur, modeles)
        logging.debug("Initialisation de l'écran de recherche")

    def _affichage_initial(self):
        logging.info("Affichage de l'écran de recherche")

    def _get_titre_ecran(self) -> str:
        return "Recherche ^YOUTUBE^"

    def fermer(self):
        logging.info("Fermeture de l'écran de recherche")
