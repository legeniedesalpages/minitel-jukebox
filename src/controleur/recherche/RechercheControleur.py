__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from typing import List, Optional

from minitel.Sequence import Sequence

from controleur.AbstractControleur import AbstractControleur
from controleur.PeutGererTouche import PeutGererTouche
from modele.JukeBoxModele import JukeBoxModele


class RechercheControleur(AbstractControleur):

    def __init__(self, controleur_pouvant_gerer_touche: List[PeutGererTouche], modeles: dict[str, object]):
        super().__init__(controleur_pouvant_gerer_touche, modeles)
        logging.debug("Initialisation du controleur de recherche")

    def _gere_touche(self, touche: Sequence) -> Optional[bool]:
        return None
