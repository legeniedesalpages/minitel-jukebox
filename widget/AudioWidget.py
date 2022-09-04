__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from minitel import Minitel
from minitel.ui.UI import UI

from controleur import JukeBoxControleur

TOUCHE_HAUT = [27, 91, 65]
TOUCHE_BAS = [27, 91, 66]


class AudioWidget(UI):

    def __init__(self, minitel: Minitel, juke_box_controleur: JukeBoxControleur):
        super().__init__(minitel, 1, 1, 1, 1, "noir")
        self.__juke_box_controleur = juke_box_controleur

    def gere_touche(self, sequence):
        touche = sequence.valeurs
        logging.debug(f"Touche appuyée: {touche}")

        if touche == TOUCHE_HAUT:
            self.__juke_box_controleur.action_augmenter_volume()
            return True

        if touche == TOUCHE_BAS:
            self.__juke_box_controleur.action_diminuer_volume()
            return True

        return False
