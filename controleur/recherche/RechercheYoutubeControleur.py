__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from controleur.recherche.AbstractRechercheControleur import AbstractRechercheControleur
from modele.JukeBoxModele import JukeBoxModele
from modele.recherche.AbstractRechercheModele import AbstractRechercheModele
from service.youtube.ChansonService import ChansonService


class RechercheYoutubeControleur(AbstractRechercheControleur):

    def __init__(self, juke_box_modele: JukeBoxModele, recherche_modele: AbstractRechercheModele):
        super().__init__(juke_box_modele, recherche_modele)
        self.__chanson_service = ChansonService()

    def lancer_recherche(self, titre_chanson):
        logging.debug(f"Lancer la recherche {self.__chanson_service}")
        liste_chanson_trouvee = self.__chanson_service.rechercher_chanson(str(titre_chanson), 17)
        self._recherche_modele.changer_liste_resultat(liste_chanson_trouvee)

    def _envoyer_lecture(self, chanson):
        logging.debug(f"Envoyer lecture => {chanson}")
