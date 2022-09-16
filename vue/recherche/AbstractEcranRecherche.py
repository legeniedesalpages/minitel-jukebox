__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
from minitel.Minitel import Minitel

from controleur.recherche.AbstractRechercheControleur import AbstractRechercheControleur
from modele.JukeBoxModele import EvenementSortieEcran
from service.MinitelConstante import TOUCHE_SOMMAIRE, TOUCHE_ENVOI, TOUCHE_BREAK
from vue.EcranInterface import EcranInterface


class AbstractEcranRecherche(EcranInterface):
    _minitel = inject.attr(Minitel)

    def __init__(self, recherche_controleur: AbstractRechercheControleur):
        self.__recherche_controleur = recherche_controleur

    def afficher(self) -> EvenementSortieEcran:

        evenement_sortie = None
        while evenement_sortie is None:
            sequence = self._minitel.recevoir_sequence(bloque=True, attente=None)
            evenement_sortie = self.gerer_touche(sequence.valeurs)

        return evenement_sortie

    def gerer_touche(self, touche):

        logging.debug(touche)

        if touche == TOUCHE_SOMMAIRE:
            logging.info("Touche Sommaire")
            return self.__recherche_controleur.changer_type_recherche()

        elif touche == TOUCHE_BREAK:
            logging.info("Touche Break")
            return self.__recherche_controleur.arreter_application()

        elif touche == TOUCHE_ENVOI:
            logging.info("Touche Envoi")
            return self.__recherche_controleur.action_envoi()

        else:
            return None
