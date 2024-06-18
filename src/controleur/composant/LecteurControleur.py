__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import logging
from typing import Optional

from minitel.Sequence import Sequence
from minitel.constantes import SUITE, RETOUR, REPETITION, ANNULATION, DROITE, GAUCHE

from controleur.commun.PeutEcouterEvenementLecteur import PeutEcouterEvenementLecteur
from controleur.commun.PeutGererTouche import PeutGererTouche
from modele.lecteur.ListeLectureModele import ListeLectureModele
from service.lecteur.AbstractLecteurService import AbstractLecteurService
from service.lecteur.PeutSuggererUneChanson import PeutSuggererUneChanson
from service.lecteur.YoutubeService import YoutubeService
from service.minitel.MinitelConstante import TOUCHE_ESPACE


class LecteurControleur(PeutGererTouche, PeutEcouterEvenementLecteur):
    __lecteur_service: Optional[AbstractLecteurService]
    __youtube_service: Optional[YoutubeService]

    def __init__(self, liste_lecture_modele: ListeLectureModele,
                 peut_suggerer_une_chanson_service: PeutSuggererUneChanson):
        self.__liste_lecture_modele = liste_lecture_modele
        self.__lecteur_service = None
        self.__peut_suggerer_une_chanson_service = peut_suggerer_une_chanson_service
        self.__youtube_service = None

    def set_youtube_service(self, youtube_service: YoutubeService):
        self.__youtube_service = youtube_service

    def definir_lecteur_service(self, lecteur_service: AbstractLecteurService):
        self.__lecteur_service = lecteur_service

    def gere_touche(self, touche: Sequence) -> Optional[bool]:
        if touche.egale(TOUCHE_ESPACE):
            self.__liste_lecture_modele.mettre_en_pause_ou_relancer_chanson(self.__lecteur_service)
            logging.info(self.__liste_lecture_modele)
            return False

        if touche.egale(SUITE):
            chanson = self.__liste_lecture_modele.jouer_chanson_suivante(self.__lecteur_service)
            if chanson is None:
                logging.info("Pas de chanson suivante")
                self.traitement_chanson_suivante()
            logging.info(self.__liste_lecture_modele)
            return False

        if touche.egale(RETOUR):
            chanson = self.__liste_lecture_modele.jouer_chanson_precedente(self.__lecteur_service)
            if chanson is None:
                logging.info("Pas de chanson précédente")
            logging.info(self.__liste_lecture_modele)
            return False

        if touche.egale(REPETITION):
            chanson = self.__liste_lecture_modele.rejouer_chanson_courante(self.__lecteur_service)
            if chanson is None:
                logging.info("Pas de chanson précédente")
            logging.info(self.__liste_lecture_modele)
            return False

        if touche.egale(ANNULATION):
            chanson = self.__liste_lecture_modele.arreter_chanson(self.__lecteur_service)
            if chanson is None:
                logging.info("Pas de chanson précédente")
            logging.info(self.__liste_lecture_modele)
            return False

        if touche.egale(DROITE):
            if self.__lecteur_service is not None:
                self.__lecteur_service.avancer()
            return False

        if touche.egale(GAUCHE):
            if self.__lecteur_service is not None:
                self.__lecteur_service.reculer()
            return False

        return None

    def evenement_progression_chanson(self, progression: int):
        self.__liste_lecture_modele.notification_progession_chanson(progression)

    def evenement_fin_chanson(self):
        self.__liste_lecture_modele.notification_arret_chanson()
        if self.__liste_lecture_modele.jouer_chanson_suivante(self.__lecteur_service) is None:
            self.traitement_chanson_suivante()

    def traitement_chanson_suivante(self):
        titre_actuel = self.__liste_lecture_modele.chanson_courante().titre
        logging.info(f"Pas de chanson suivante, on va en chercher une en se basant sur: {titre_actuel}")
        suggestion = self.__peut_suggerer_une_chanson_service.suggestion(titre_actuel)
        logging.info(f"Suggestion de chanson: {suggestion}")
        chansons = self.__youtube_service.rechercher_chanson(suggestion)
        if len(chansons) > 0:
            self.__liste_lecture_modele.ajouter_chanson(chansons[0])
            self.__liste_lecture_modele.jouer_chanson_suivante(self.__lecteur_service)
        else:
            logging.info("Pas de chanson trouvée pour la suggestion")
