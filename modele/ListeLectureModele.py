__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from typing import List

from modele.Chanson import Chanson


class ListeLectureModele:

    __liste_lecture: List[Chanson]

    def __init__(self):
        self.__liste_lecture = []
        self.__index = 0

    def ajouter_chanson(self, chanson):
        self.__liste_lecture.append(chanson)

    def inserer_chanson(self, chanson):
        self.__liste_lecture.insert(self.__index,chanson)

    def avancer_chanson(self) -> Chanson:
        if self.__index < len(self.__liste_lecture):
            self.__index += 1

    def reculer_chanson(self) -> Chanson:
        if self.__index > 0:
            self.__index -= 1
