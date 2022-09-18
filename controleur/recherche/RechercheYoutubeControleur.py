__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from controleur.recherche.AbstractRechercheControleur import AbstractRechercheControleur
from modele.JukeBoxModele import JukeBoxModele, EvenementSortieEcran
from modele.recherche.RechercheYoutubeModele import RechercheYoutubeModele


class RechercheYoutubeControleur(AbstractRechercheControleur):

    def __init__(self, juke_box_modele: JukeBoxModele, recherche_youtube_modele: RechercheYoutubeModele):
        super().__init__(juke_box_modele)
        logging.debug("Initialisation du controleur de la recherche par Youtube")
        self.__recherche_youtube_modele = recherche_youtube_modele

    def action_envoi(self) -> EvenementSortieEcran:
        logging.info("On va lancer la chanson et aller sur le visualiseur")
        print(self.__recherche_youtube_modele)
        return EvenementSortieEcran.VISUALISER_CHANSON
