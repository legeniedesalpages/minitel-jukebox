__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from enum import Enum, auto
from typing import List

import inject
from pyobservable import Observable

from modele.Chanson import Chanson
from modele.JukeBoxModele import EvenementSortieEcran


class MouvementSelection(Enum):
    MONTE = auto()
    DESCEND = auto()
    PAGE = auto()


class AbstractRechercheModele:
    __notificateur_evenement = inject.attr(Observable)

    EVENEMENT_CHANGEMENT_RESULTAT = "EvenementChangementResultat"
    EVENEMENT_CHANGEMENT_SELECTION = "EvenementChangementSelection"

    evenement_sortie: EvenementSortieEcran
    liste_resultat: List[Chanson]
    element_selectionne: int

    def __init__(self):
        self.evenement_sortie = EvenementSortieEcran.PAS_DE_SORTIE

    def changer_liste_resultat(self, nouvelle_liste_resultat):
        self.liste_resultat = nouvelle_liste_resultat
        self.element_selectionne = 1
        self.__notificateur_evenement.notify(AbstractRechercheModele.EVENEMENT_CHANGEMENT_RESULTAT)

    def resultat_recherche_suivant(self):
        if self.element_selectionne < len(self.liste_resultat):
            self.element_selectionne += 1
            self.__notificateur_evenement.notify(AbstractRechercheModele.EVENEMENT_CHANGEMENT_SELECTION,
                                                 MouvementSelection.DESCEND)

    def resultat_recherche_precedent(self):
        if self.element_selectionne > 1:
            self.element_selectionne -= 1
            self.__notificateur_evenement.notify(AbstractRechercheModele.EVENEMENT_CHANGEMENT_SELECTION,
                                                 MouvementSelection.MONTE)
