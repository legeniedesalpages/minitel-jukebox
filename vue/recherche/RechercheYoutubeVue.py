__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from controleur.recherche import RechercheYoutubeControleur
from modele.JukeBoxModele import EvenementSortieEcran
from modele.recherche.RechercheYoutubeModele import RechercheYoutubeModele
from vue.recherche.AbstractEcranRecherche import AbstractEcranRecherche


class RechercheYoutubeVue(AbstractEcranRecherche):

    def __init__(self, recherche_controleur: RechercheYoutubeControleur, recherche_modele: RechercheYoutubeModele):
        super().__init__(recherche_controleur)
        logging.debug("Initialisation de la vue de la recherche Youtube")
        self.__recherche_controleur = recherche_controleur
        self.__recherche_modele = recherche_modele

    def afficher(self) -> EvenementSortieEcran:
        self._minitel.position(1, 1)
        self._minitel.envoyer('Recherche dans les services Youtube')

        return super().afficher()
