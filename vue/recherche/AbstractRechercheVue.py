__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
from minitel.Minitel import Minitel
from minitel.constantes import SOMMAIRE, ENVOI
from minitel.ui.Conteneur import Conteneur

from controleur.recherche.AbstractRechercheControleur import AbstractRechercheControleur
from modele.JukeBoxModele import EvenementSortieEcran
from modele.recherche.AbstractRechercheModele import AbstractRechercheModele
from service.minitel.MinitelExtension import MinitelExtension
from vue.EcranInterface import EcranInterface
from vue.composant.AudioComposantVue import AudioComposantVue


class AbstractRechercheVue(EcranInterface):
    _minitel_extension = inject.attr(MinitelExtension)
    _minitel = inject.attr(Minitel)
    _conteneur: Conteneur

    def __init__(self, recherche_controleur: AbstractRechercheControleur, recherche_modele: AbstractRechercheModele):
        self.__recherche_controleur = recherche_controleur
        self.__recherche_youtube_modele = recherche_modele
        self._conteneur = Conteneur(self._minitel, 1, 1, 1, 1)

        self._conteneur.ajoute(AudioComposantVue(self._minitel, self._conteneur))

    def afficher(self):
        logging.info("Affichage de la recherche Youtube")
        self._conteneur.affiche()
        self.__gerer_boucle()
        self._conteneur.efface()

    def fermer(self):
        logging.info("Ferme la recherche Youtube")
        for element in self._conteneur.elements:
            element.efface()

    def __gerer_boucle(self):

        while self.__recherche_youtube_modele.evenement_sortie is EvenementSortieEcran.PAS_DE_SORTIE:
            sequence = self._minitel.recevoir_sequence(bloque=True, attente=None)
            self.__gerer_touche(sequence)

    def _gerer_touche(self, sequence):
        pass

    def __gerer_touche(self, sequence):

        if sequence.egale(SOMMAIRE):
            logging.debug("Touche gérée par la vue générique")
            self.__recherche_controleur.changer_type_recherche()
            return

        if sequence.egale(ENVOI):
            logging.debug("Touche gérée par la vue générique")
            self.__recherche_controleur.envoyer_chanson()
            return

        if self._gerer_touche(sequence):
            logging.debug("Touche gérée par l'écran")
            return

        if self._conteneur.element_actif is not None and self._conteneur.element_actif.gere_touche(sequence):
            logging.debug("Touche gérée par l'element actif")
            return

        for element in self._conteneur.elements:
            if element is not self._conteneur.element_actif:
                if element.gere_touche(sequence):
                    logging.debug("Touche gérée par un elément du conteneur")
                    return

        logging.debug(f"Touche non gérée: {sequence.valeurs}")
