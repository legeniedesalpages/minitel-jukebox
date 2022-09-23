__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from enum import Enum, auto
from typing import List

import inject
import math
from pyobservable import Observable

from modele.Chanson import Chanson
from modele.JukeBoxModele import EvenementSortieEcran


class MouvementSelection(Enum):
    MONTE = auto()
    DESCEND = auto()
    PAGE = auto()


class EvenementRechercheModele(Enum):
    EVENEMENT_CHANGEMENT_RESULTAT = auto()
    EVENEMENT_CHANGEMENT_SELECTION = auto()
    EVENEMENT_ANNULATION_RECHERCHE = auto()


class AbstractRechercheModele:
    TAILLE_PAGE_RECHERCHE = 5

    __notificateur_evenement = inject.attr(Observable)

    evenement_sortie: EvenementSortieEcran
    liste_resultat: List[Chanson]
    element_selectionne: int

    def __init__(self):
        self.evenement_sortie = EvenementSortieEcran.PAS_DE_SORTIE

    def changer_liste_resultat(self, nouvelle_liste_resultat):
        self.liste_resultat = nouvelle_liste_resultat
        self.element_selectionne = 1
        self.__notificateur_evenement.notify(EvenementRechercheModele.EVENEMENT_CHANGEMENT_RESULTAT)

    def resultat_recherche_suivant(self):
        if self.element_selectionne < len(self.liste_resultat):
            self.element_selectionne += 1
            self.__notificateur_evenement.notify(EvenementRechercheModele.EVENEMENT_CHANGEMENT_SELECTION,
                                                 MouvementSelection.DESCEND)

    def resultat_recherche_precedent(self):
        if self.element_selectionne > 1:
            self.element_selectionne -= 1
            self.__notificateur_evenement.notify(EvenementRechercheModele.EVENEMENT_CHANGEMENT_SELECTION,
                                                 MouvementSelection.MONTE)

    def resultat_recherche_page_suivante(self):
        element_page_suivante = math.ceil(self.element_selectionne / 5) * 5 + 1
        if element_page_suivante < len(self.liste_resultat) + 1:
            self.element_selectionne = element_page_suivante
            self.__notificateur_evenement.notify(EvenementRechercheModele.EVENEMENT_CHANGEMENT_SELECTION,
                                                 MouvementSelection.PAGE)

    def resultat_recherche_page_precedente(self):
        element_page_precedente = (math.ceil(self.element_selectionne / 5) - 2) * 5 + 1
        if element_page_precedente >= 1:
            self.element_selectionne = element_page_precedente
            self.__notificateur_evenement.notify(EvenementRechercheModele.EVENEMENT_CHANGEMENT_SELECTION,
                                                 MouvementSelection.PAGE)

    def annuler_recherche(self, conserver_texte_saisie):
        self.element_selectionne = 0
        self.__notificateur_evenement.notify(EvenementRechercheModele.EVENEMENT_ANNULATION_RECHERCHE,
                                             conserver_texte_saisie)
