__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from minitel.ui.ChampTexte import ChampTexte

from controleur.recherche import RechercheYoutubeControleur
from modele.JukeBoxModele import EvenementSortieEcran
from modele.recherche.RechercheYoutubeModele import RechercheYoutubeModele
from service.MinitelConstante import TOUCHE_ENVOI
from vue.recherche.AbstractEcranRecherche import AbstractEcranRecherche


class RechercheYoutubeVue(AbstractEcranRecherche):
    __recherche_controleur: RechercheYoutubeControleur

    def __init__(self, recherche_controleur: RechercheYoutubeControleur, recherche_modele: RechercheYoutubeModele):
        super().__init__(recherche_controleur)
        logging.debug("Initialisation de la vue de la recherche Youtube")
        self.__recherche_controleur = recherche_controleur
        self.__recherche_modele = recherche_modele
        self.__champ = None

    def afficher(self) -> EvenementSortieEcran:
        super().afficher()
        self._minitel.position(1, 1)
        self._minitel.envoyer("Recherche dans les services ")
        self._minitel.effet(inversion=True)
        self._minitel.envoyer("Youtube")
        self._minitel.position(2, 3)
        self._minitel.couleur("vert")
        self._minitel.envoyer("Chanson:")
        self.__champ = ChampTexte(self._minitel, 10, 3, 25, 60)
        self.__champ.affiche()

        return super().gerer_boucle()

    def fermer(self):
        super().fermer()

    def gerer_touche(self, touche) -> EvenementSortieEcran:
        self.__champ

        if touche == TOUCHE_ENVOI:
            logging.info("Touche Envoi")
            return self.__recherche_controleur.action_envoi()
