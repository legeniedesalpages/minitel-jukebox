__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from modele.JukeBoxModele import JukeBoxModele, EvenementSortieEcran
from vue.EcranInterface import EcranInterface


class AbstractRechercheControleur:
    __ecran_recherche_interface: EcranInterface

    def __init__(self, juke_box_modele: JukeBoxModele):
        logging.debug("Initialisation du controleur générique")
        self.__juke_box_modele = juke_box_modele

    def enregistrer_vue(self, ecran_recherche_interface):
        self.__ecran_recherche_interface = ecran_recherche_interface

    def afficher_ecran_recherche(self) -> EvenementSortieEcran:
        evenement_sortie = self.__ecran_recherche_interface.afficher()
        # afficher() est bloquant
        self.__ecran_recherche_interface.fermer()

        return evenement_sortie

    def changer_type_recherche(self) -> EvenementSortieEcran:
        self.__juke_box_modele.changer_recherche()
        return EvenementSortieEcran.AFFICHER_RECHERCHE

    @staticmethod
    def arreter_application() -> EvenementSortieEcran:
        return EvenementSortieEcran.ARRETER_APPLICATION
