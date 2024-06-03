__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
import typing
from enum import auto, Enum
from typing import List

import inject
from pyobservable import Observable

from modele.Chanson import Chanson
from service.AbstractLecteurService import AbstractLecteurService


# noinspection PyArgumentList
class EtatLecture(Enum):
    STOP = auto(),
    PAUSE = auto(),
    JOUE = auto()


# noinspection PyArgumentList
class ModeRepetition(Enum):
    PAS_DE_REPETITION = auto(),
    UNE_SEULE_CHANSON = auto(),
    TOUTE_LA_LISTE = auto()


# noinspection PyArgumentList
class ModeLecture(Enum):
    ALEATOIRE = auto(),
    DANS_L_ORDRE = auto()


class ListeLectureModele:
    EVENEMENT_LECTURE_STOP = "evenementLectureStop"
    EVENEMENT_LECTURE_PAUSE = "evenementLecturePause"
    EVENEMENT_LECTURE_JOUE = "evenementLectureJoue"
    EVENEMENT_LECTURE_CHANGE_CHANSON = "evenementLectureChangeChanson"
    EVENEMENT_LECTURE_PROGRESSE = "evenementLectureProgresse"

    __notificateur_evenement = inject.attr(Observable)

    __liste_lecture: List[Chanson]
    progression_chanson_courante: typing.Optional[int]
    etat_lecture: EtatLecture

    def __init__(self):
        self.__liste_lecture = []
        self.__index_courant = 0
        self.progression_chanson_courante = None
        self.etat_lecture = EtatLecture.STOP

    def ajouter_chanson(self, chanson):
        self.__liste_lecture.append(chanson)

    def etat_courant(self) -> str:
        liste = "".join(map(lambda chanson: "'" + chanson.titre + "',", self.__liste_lecture))
        courant = self.chanson_courante()
        if courant is None:
            courant = "Aucune"
        else:
            courant = courant.titre
        return f"{courant}({self.etat_lecture.name}) [{liste}] ({self.__index_courant})"

    def inserer_puis_jouer_chanson(self, chanson, lecteur_service: AbstractLecteurService):
        if self.etat_lecture != EtatLecture.STOP:
            self.arreter_chanson(lecteur_service)
            self.__index_courant += 1

        self.__liste_lecture.insert(self.__index_courant, chanson)
        self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_CHANGE_CHANSON)

        return self.jouer_chanson_courante(lecteur_service)

    def arreter_chanson(self, lecteur_service: AbstractLecteurService):
        if self.etat_lecture != EtatLecture.STOP:
            lecteur_service.arreter()
            self.etat_lecture = EtatLecture.STOP
            self.progression_chanson_courante = None
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_STOP)

    def rejouer_chanson_courante(self, lecteur_service: AbstractLecteurService) -> Chanson:
        if self.etat_lecture != EtatLecture.STOP:
            self.arreter_chanson(lecteur_service)
        return self.jouer_chanson_courante(lecteur_service)

    def jouer_chanson_suivante(self, lecteur_service: AbstractLecteurService) -> typing.Optional[Chanson]:
        if self.__index_courant < len(self.__liste_lecture)-1:
            if self.etat_lecture != EtatLecture.STOP:
                lecteur_service.arreter()
            self.__index_courant += 1
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_CHANGE_CHANSON)
            return self.jouer_chanson_courante(lecteur_service)
        return None

    def jouer_chanson_precedente(self, lecteur_service: AbstractLecteurService) -> typing.Optional[Chanson]:
        if self.__index_courant > 0:
            if self.etat_lecture != EtatLecture.STOP:
                lecteur_service.arreter()
            self.__index_courant -= 1
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_CHANGE_CHANSON)
            return self.jouer_chanson_courante(lecteur_service)

        return None

    def chanson_courante(self) -> typing.Optional[Chanson]:
        logging.warning(f"index chanson de la liste de lecture: {self.__index_courant}, taille de la liste: {len(self.__liste_lecture)}")
        if len(self.__liste_lecture) == 0:
            return None

        return self.__liste_lecture[self.__index_courant]

    def mettre_en_pause_ou_relancer_chanson(self, lecteur_service: AbstractLecteurService):
        if self.etat_lecture == EtatLecture.STOP:
            return

        if self.etat_lecture == EtatLecture.JOUE:
            lecteur_service.pause()
            self.etat_lecture = EtatLecture.PAUSE
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_PAUSE)
        else:
            lecteur_service.relance()
            self.etat_lecture = EtatLecture.JOUE
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_JOUE)

    def jouer_chanson_courante(self, lecteur_service: AbstractLecteurService) -> Chanson:
        lecteur_service.jouer(self.chanson_courante())
        self.progression_chanson_courante = 0
        self.etat_lecture = EtatLecture.JOUE
        self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_JOUE)
        return self.chanson_courante()

    def notification_progession_chanson(self, progression: int):
        if self.progression_chanson_courante is None:
            self.progression_chanson_courante = progression
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_PROGRESSE)
        elif self.progression_chanson_courante != progression:
            self.progression_chanson_courante = progression
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_PROGRESSE)

    def notification_arret_chanson(self):
        self.progression_chanson_courante = None
        self.etat_lecture = EtatLecture.STOP
        self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_STOP)
