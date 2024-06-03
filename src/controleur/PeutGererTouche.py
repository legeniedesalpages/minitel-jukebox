__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import abc
from typing import Optional

from minitel.Sequence import Sequence


class PeutGererTouche:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def gere_touche(self, touche: Sequence) -> Optional[bool]:
        """Gère une touche pressée par l'utilisateur
        :returns:
            None : la touche n'est pas gérée
            False : la touche est gérée mais le traitement doit continuer
            True : la touche est gérée et le traitement doit s'arrêter"""
        pass
