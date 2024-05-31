__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from controleur.recherche.RechercheControleur import RechercheControleur
from vue.AbstractEcran import AbstractEcran


class EcranRecherche(AbstractEcran):

    def __init__(self, recherche_controleur: RechercheControleur, modeles: dict[str, object]):
        super().__init__(recherche_controleur, modeles)
        logging.debug(f"Initialisation de l'écran de recherche {self._minitel}")

    def _affichage_initial(self):
        logging.info("Affichage de l'écran de recherche")

    def _get_titre_ecran(self) -> str:
        return "Recherche ^YOUTUBE^"

    def _get_callback_curseur(self):
        pass

    def fermer(self):
        logging.info("Fermeture de l'écran de recherche")
