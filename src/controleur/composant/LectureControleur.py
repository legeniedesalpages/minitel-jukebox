__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

from typing import Optional

from minitel.Sequence import Sequence

from controleur.PeutGererTouche import PeutGererTouche


class LectureControleur(PeutGererTouche):

    def gere_touche(self, touche: Sequence) -> Optional[bool]:
        return None
