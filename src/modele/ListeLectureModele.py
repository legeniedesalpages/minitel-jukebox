__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
import typing
from enum import auto, Enum
from typing import List

from modele.Chanson import Chanson
from modele.RecuperateurChanson import RecuperateurChanson


class ModeRepetition(Enum):
    PAS_DE_REPETITION = auto(),
    UNE_SEULE_CHANSON = auto(),
    TOUTE_LA_LISTE = auto()


class ModeLecture(Enum):
    ALEATOIRE = auto(),
    AVANCE = auto()


class ListeLectureModele:
    __liste_lecture: List[Chanson]

    def __init__(self, recuperateur_chanson: RecuperateurChanson, mode_repetition: ModeRepetition,
                 mode_lecture: ModeLecture):
        self.__liste_lecture = []
        self.__index = 0

    def ajouter_chanson(self, chanson):
        self.__liste_lecture.append(chanson)

    def inserer_chanson(self, chanson):
        self.__liste_lecture.insert(self.__index, chanson)

    def chanson_suivante(self) -> typing.Optional[Chanson]:
        if self.__index < len(self.__liste_lecture):
            self.__index += 1
            return self.chanson_courante()
        else:
            return None

    def chanson_precedente(self) -> typing.Optional[Chanson]:
        if self.__index > 1:
            self.__index -= 1
            return self.chanson_courante()
        else:
            return None

    def chanson_courante(self) -> typing.Optional[Chanson]:
        logging.info(f"index chanson de la liste de lecture: {self.__index}")
        if self.__index == 0:
            return None
        else:
            return self.__liste_lecture[self.__index - 1]
