__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from modele.Chanson import Chanson
from modele.JukeBoxModele import JukeBoxModele, EvenementSortieEcran
from modele.recherche.AbstractRechercheModele import AbstractRechercheModele
from vue.EcranInterface import EcranInterface


class AbstractRechercheControleur:
    __ecran_recherche_interface: EcranInterface

    def __init__(self, juke_box_modele: JukeBoxModele, recherche_modele: AbstractRechercheModele):
        logging.debug("Initialisation du controleur générique")
        self.__juke_box_modele = juke_box_modele
        self._recherche_modele = recherche_modele

    def enregistrer_vue(self, ecran_recherche_interface):
        self.__ecran_recherche_interface = ecran_recherche_interface

    def afficher_ecran_recherche(self) -> EvenementSortieEcran:
        self.__ecran_recherche_interface.afficher()
        # afficher() est bloquant
        self.__ecran_recherche_interface.fermer()

        return self._recherche_modele.evenement_sortie

    def changer_type_recherche(self):
        logging.debug("Changement du type de recherche")
        self.__juke_box_modele.changer_recherche()
        self._recherche_modele.evenement_sortie = EvenementSortieEcran.AFFICHER_RECHERCHE

    def afficher_configuration_bluetooth(self):
        self._recherche_modele.evenement_sortie = EvenementSortieEcran.CONFIGURATION_BLUETOOTH

    def envoyer_lecture(self):
        self._envoyer_lecture(self._recherche_modele.liste_resultat[self._recherche_modele.element_selectionne - 1])
        self._recherche_modele.evenement_sortie = EvenementSortieEcran.VISUALISER_CHANSON

    def _envoyer_lecture(self, element: Chanson):
        pass

    def chanson_selectionne(self):
        return self._recherche_modele.liste_resultat[self._recherche_modele.element_selectionne - 1]

    def lancer_recherche(self, texte_a_chercher, nombre_a_cherche):
        pass

    def chercher_et_lire(self, texte_a_chercher):
        self._recherche_modele.evenement_sortie = EvenementSortieEcran.VISUALISER_CHANSON
        self.lancer_recherche(texte_a_chercher, 1)
        self._envoyer_lecture(self._recherche_modele.liste_resultat[0])

    def arreter_application(self):
        self._recherche_modele.evenement_sortie = EvenementSortieEcran.ARRETER_APPLICATION

    def resultat_recherche_suivant(self):
        self._recherche_modele.resultat_recherche_suivant()

    def resultat_recherche_precedent(self):
        self._recherche_modele.resultat_recherche_precedent()

    def resultat_recherche_page_suivante(self):
        self._recherche_modele.resultat_recherche_page_suivante()

    def resultat_recherche_page_precedente(self):
        self._recherche_modele.resultat_recherche_page_precedente()

    def annuler_recherche(self, conserver_texte_saisie):
        logging.debug("Annule la recherche")
        self._recherche_modele.annuler_recherche(conserver_texte_saisie)
