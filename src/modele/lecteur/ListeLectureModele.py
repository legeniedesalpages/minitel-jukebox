__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
import random
import typing
from enum import auto, Enum
from typing import List

from pyobservable import Observable

from modele.lecteur.Chanson import Chanson
from service.lecteur.AbstractLecteurService import AbstractLecteurService


# noinspection PyArgumentList
class EtatLecture(Enum):
    STOP = auto(),
    PAUSE = auto(),
    JOUE = auto(),
    CHARGEMENT = auto()


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
    EVENEMENT_LECTURE_CHARGEMENT = "evenementLectureChargement"

    liste_lecture: List[Chanson]
    progression_chanson_courante: typing.Optional[int]
    etat_lecture: EtatLecture
    index_courant: int

    def __init__(self, notificateur_evenement: Observable):
        self.liste_lecture = []
        self.index_courant = 0
        self.__notificateur_evenement = notificateur_evenement
        self.progression_chanson_courante = None
        self.etat_lecture = EtatLecture.STOP

    def ajouter_au_hasard(self, liste_chansons: List[Chanson]):
        random.shuffle(liste_chansons)
        self.liste_lecture = liste_chansons
        self.index_courant = 0

    def ajouter_chanson(self, chanson):
        """
        insère une chanson à la fin de la liste de lecture
        :param chanson:
        """
        self.liste_lecture.append(chanson)
        logging.debug(
            f"ajouter chanson: index chanson de la liste de lecture: {self.index_courant}, taille de la liste: {len(self.liste_lecture)}")

    def inserer_puis_jouer_chanson(self, chanson, lecteur_service: AbstractLecteurService):
        """
        Insérer une chanson dans la liste de lecture puis la jouer. Si une chanson est en cours de lecture, elle est arrêtée et la chanson à insérer sera mise juste après.
        Si aucune chanson n'est en cours de lecture, la chanson à insérer avant la chanson qui aurait été jouée puis elle est jouée
        :param chanson:
        :param lecteur_service:
        :return:
        """
        if self.etat_lecture != EtatLecture.STOP:
            self.arreter_chanson(lecteur_service)
            self.index_courant += 1

        self.liste_lecture.insert(self.index_courant, chanson)
        self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_CHANGE_CHANSON)

        return self.jouer_chanson_courante(lecteur_service)

    def arreter_chanson(self, lecteur_service: AbstractLecteurService):
        if self.etat_lecture != EtatLecture.STOP:
            lecteur_service.arreter()
            self.etat_lecture = EtatLecture.STOP
            self.progression_chanson_courante = None
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_STOP)

    def rejouer_chanson_courante(self, lecteur_service: AbstractLecteurService) -> typing.Optional[Chanson]:
        """
        Rejouer la chanson courante
        :param lecteur_service:
        :return: la chanson qui va être rejouée ou None si il n'y a pas de chanson courante
        """
        logging.debug("Rejouer la chanson courante")
        if self.etat_lecture != EtatLecture.STOP:
            self.arreter_chanson(lecteur_service)
        return self.jouer_chanson_courante(lecteur_service)

    def jouer_chanson_suivante(self, lecteur_service: AbstractLecteurService) -> typing.Optional[Chanson]:
        """
        Joue la chanson suivante
        :param lecteur_service:
        :return: la chanson qui va être jouée ou None si il n'y a pas de chanson suivante
        """
        if self.index_courant < len(self.liste_lecture) - 1:
            logging.debug(
                f"Chanson suivante => index : {self.index_courant}, taille de la liste: {len(self.liste_lecture)}")
            if self.etat_lecture != EtatLecture.STOP:
                logging.debug("Une chanson était en cours: arret de cette chanson pour pouvoir jouer la suivante")
                lecteur_service.arreter()
            self.index_courant += 1
            lecteur_service.preparer_chanson(self.liste_lecture[self.index_courant])
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_CHANGE_CHANSON)
            return self.jouer_chanson_courante(lecteur_service)

        logging.debug(
            f"Pas de chanson suivante à jouer, la liste ({len(self.liste_lecture)}) n'est pas assez grande pour l'index {self.index_courant}")
        return None

    def jouer_chanson_precedente(self, lecteur_service: AbstractLecteurService) -> typing.Optional[Chanson]:
        """
        Joue la chanson précédente,
        :param lecteur_service:
        :return: la chanson qui va être jouée ou None si il n'y a pas de chanson précédente
        """
        if self.index_courant > 0:
            if self.etat_lecture != EtatLecture.STOP:
                lecteur_service.arreter()
            self.index_courant -= 1
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_CHANGE_CHANSON)
            return self.jouer_chanson_courante(lecteur_service)

        return None

    def chanson_courante(self) -> typing.Optional[Chanson]:
        """
        Récupérer la chanson courante
        :return: la chanson courante ou None si il n'y a aucune chanson dans la liste
        """
        logging.debug(
            f"Récupérer la chanson courante => index: {self.index_courant}, taille de la liste: {len(self.liste_lecture)}")
        if len(self.liste_lecture) == 0:
            return None

        return self.liste_lecture[self.index_courant]

    def mettre_en_pause_ou_relancer_chanson(self, lecteur_service: AbstractLecteurService) -> typing.Optional[bool]:
        """
        Mettre en pause ou relancer la chanson courante
        :param lecteur_service:
        :return: None si pas de chanson courante, True si la chanson est en pause, False si la chanson est remise en route
        """
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

    def jouer_chanson_courante(self, lecteur_service: AbstractLecteurService) -> typing.Optional[Chanson]:
        """
        Jouer la chanson courante
        :return: la chanson courante si elle a été jouée, None s'il n'y avait pas de chanson courante
        """
        chanson_courante = self.chanson_courante()
        logging.debug("Jouer la chanson courante: " + str(chanson_courante))
        if chanson_courante is not None:
            self.etat_lecture = EtatLecture.CHARGEMENT
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_CHARGEMENT)
            lecteur_service.jouer(self.chanson_courante())
            self.progression_chanson_courante = 0
            self.etat_lecture = EtatLecture.JOUE
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_JOUE)
            return chanson_courante
        return None

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
        self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_PROGRESSE)
        self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_STOP)

    def jouer_chanson_a_index(self, index: int, lecteur_service: AbstractLecteurService):
        logging.info(f"On essaye de jouer la chanson à l'index: {index}")
        if 0 <= index < len(self.liste_lecture):
            self.index_courant = index
            self.__notificateur_evenement.notify(self.EVENEMENT_LECTURE_CHANGE_CHANSON)
            self.rejouer_chanson_courante(lecteur_service)

    def __str__(self) -> str:
        liste = "".join(map(lambda chanson: "'" + chanson.titre + "',", self.liste_lecture))
        courant = self.chanson_courante()
        if courant is None:
            courant = "Aucune"
        else:
            courant = courant.titre
        return f"{courant}({self.etat_lecture.name}) [{liste}] ({self.index_courant})"
