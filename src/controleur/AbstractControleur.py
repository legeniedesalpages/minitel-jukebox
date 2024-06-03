__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import abc
import logging
from typing import List, Optional

from minitel.Sequence import Sequence

from controleur.PeutGererTouche import PeutGererTouche
from vue.Affichable import Affichable


class AbstractControleur:
    __metaclass__ = abc.ABCMeta

    _vue: Optional[Affichable]

    def __init__(self, controleurs_pouvant_gerer_touche: dict[str, PeutGererTouche], modeles: dict[str, object]):
        logging.debug("Controleur générique créé")
        self._controleur_pouvant_gerer_touche: List[PeutGererTouche] = list(controleurs_pouvant_gerer_touche.values())

    def gere_touche(self, sequence: Sequence) -> Optional[bool]:
        gestion_specifique = self._gere_touche(sequence)
        logging.debug(f"Controleur générique gere_touche {gestion_specifique}")
        if gestion_specifique is None:
            for controleur_pouvant_gerer_toucher in self._controleur_pouvant_gerer_touche:
                retour = controleur_pouvant_gerer_toucher.gere_touche(sequence)
                logging.debug(f"Controleur générique gere_touche {retour} de {controleur_pouvant_gerer_toucher}")
                if retour is not None:
                    return retour
        else:
            return gestion_specifique

        return None

    def enregistrer_vue(self, vue: Affichable):
        self._vue = vue

    @abc.abstractmethod
    def lancer(self):
        self._vue.afficher()

    @abc.abstractmethod
    def _gere_touche(self, touche: Sequence) -> Optional[bool]:
        return None
