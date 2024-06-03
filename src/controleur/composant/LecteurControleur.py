__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import logging
from typing import Optional

from minitel.Sequence import Sequence
from minitel.constantes import SUITE, RETOUR, REPETITION, ANNULATION

from controleur.PeutEcouterEvenementLecteur import PeutEcouterEvenementLecteur
from controleur.PeutGererTouche import PeutGererTouche
from modele.ListeLectureModele import ListeLectureModele
from service.AbstractLecteurService import AbstractLecteurService
from service.minitel.MinitelConstante import TOUCHE_ESPACE


class LecteurControleur(PeutGererTouche, PeutEcouterEvenementLecteur):
    __lecteur_service: Optional[AbstractLecteurService]

    def __init__(self, liste_lecture_modele: ListeLectureModele):
        self.__liste_lecture_modele = liste_lecture_modele

    def definir_lecteur_service(self, lecteur_service: AbstractLecteurService):
        self.__lecteur_service = lecteur_service

    def gere_touche(self, touche: Sequence) -> Optional[bool]:
        if touche.egale(TOUCHE_ESPACE):
            self.__liste_lecture_modele.mettre_en_pause_ou_relancer_chanson(self.__lecteur_service)
            logging.warning(self.__liste_lecture_modele.etat_courant())
            return False

        if touche.egale(SUITE):
            chanson_suivante = self.__liste_lecture_modele.jouer_chanson_suivante(self.__lecteur_service)
            if chanson_suivante is None:
                logging.info("Pas de chanson suivante")
            logging.warning(self.__liste_lecture_modele.etat_courant())
            return False

        if touche.egale(RETOUR):
            chanson_suivante = self.__liste_lecture_modele.jouer_chanson_precedente(self.__lecteur_service)
            if chanson_suivante is None:
                logging.info("Pas de chanson précédente")
            logging.warning(self.__liste_lecture_modele.etat_courant())
            return False

        if touche.egale(REPETITION):
            chanson_suivante = self.__liste_lecture_modele.rejouer_chanson_courante(self.__lecteur_service)
            if chanson_suivante is None:
                logging.info("Pas de chanson précédente")
            logging.warning(self.__liste_lecture_modele.etat_courant())
            return False

        if touche.egale(ANNULATION):
            chanson_suivante = self.__liste_lecture_modele.arreter_chanson(self.__lecteur_service)
            if chanson_suivante is None:
                logging.info("Pas de chanson précédente")
            logging.warning(self.__liste_lecture_modele.etat_courant())
            return False

        return None

    def evenement_progression_chanson(self, progression: int):
        self.__liste_lecture_modele.notification_progession_chanson(progression)

    def evenement_fin_chanson(self):
        self.__liste_lecture_modele.notification_arret_chanson()
