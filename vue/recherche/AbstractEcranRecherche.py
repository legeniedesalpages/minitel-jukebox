__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from typing import List

import inject
from minitel.Minitel import Minitel

from controleur.recherche.AbstractRechercheControleur import AbstractRechercheControleur
from modele.JukeBoxModele import EvenementSortieEcran
from service.MinitelConstante import TOUCHE_SOMMAIRE, TOUCHE_BREAK
from vue.EcranInterface import EcranInterface
from vue.composant.AudioComposantVue import AudioComposantVue
from vue.composant.InterfaceComposantVue import InterfaceComposantVue


class AbstractEcranRecherche(EcranInterface):
    _minitel = inject.attr(Minitel)
    __composant_audio = inject.attr(AudioComposantVue)

    def __init__(self, recherche_controleur: AbstractRechercheControleur):
        self.__recherche_controleur = recherche_controleur
        self.__liste_composant: List[InterfaceComposantVue] = list()
        self._ajouter_composant(self.__composant_audio)

    def afficher(self) -> EvenementSortieEcran:
        for composant in self.__liste_composant:
            composant.afficher()
        return EvenementSortieEcran.PAS_DE_SORTIE

    def fermer(self):
        for composant in self.__liste_composant:
            composant.fermer()

    def _ajouter_composant(self, composant: InterfaceComposantVue):
        self.__liste_composant.append(composant)

    def gerer_boucle(self) -> EvenementSortieEcran:

        evenement_sortie = EvenementSortieEcran.PAS_DE_SORTIE
        while evenement_sortie is EvenementSortieEcran.PAS_DE_SORTIE:
            sequence = self._minitel.recevoir_sequence(bloque=True, attente=None)
            evenement_sortie = self.__gerer_touche(sequence.valeurs)

        return evenement_sortie

    def __gerer_touche(self, touche) -> EvenementSortieEcran:

        logging.debug(f"Appuie sur la touche: {touche}")

        if touche == TOUCHE_SOMMAIRE:
            logging.info("Touche Sommaire")
            return self.__recherche_controleur.changer_type_recherche()

        elif touche == TOUCHE_BREAK:
            logging.info("Touche Break")
            return self.__recherche_controleur.arreter_application()

        else:
            for composant in self.__liste_composant:
                if composant.gere_touche(touche):
                    return EvenementSortieEcran.PAS_DE_SORTIE

            evenement = self.gerer_touche(touche)
            if evenement is None:
                return EvenementSortieEcran.PAS_DE_SORTIE
            else:
                return evenement
