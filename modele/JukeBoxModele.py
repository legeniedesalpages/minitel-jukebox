__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from enum import Enum, auto


class TypeRecherche(Enum):
    YOUTUBE = auto()
    SPOTIFY = auto()
    REPERTOIRE = auto()
    HISTORIQUE = auto()


class EvenementSortieEcran(Enum):
    PAS_DE_SORTIE = auto()
    AFFICHER_RECHERCHE = auto()
    VISUALISER_CHANSON = auto()
    ARRETER_APPLICATION = auto()


class JukeBoxModele:

    def __init__(self, type_recherche: TypeRecherche):
        logging.debug("Initialisation du modele de la recherche")
        self.type_recherche = type_recherche

    def changer_recherche(self):

        if self.type_recherche == TypeRecherche.YOUTUBE:
            self.type_recherche = TypeRecherche.SPOTIFY

        elif self.type_recherche == TypeRecherche.SPOTIFY:
            self.type_recherche = TypeRecherche.YOUTUBE
