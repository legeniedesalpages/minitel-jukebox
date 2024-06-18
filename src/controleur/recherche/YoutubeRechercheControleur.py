__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from typing import Optional

import inject
from minitel.Sequence import Sequence
from minitel.constantes import ENVOI, ENTREE
from pyobservable import Observable

from controleur.commun.AbstractControleur import AbstractControleur
from controleur.commun.PeutGererTouche import PeutGererTouche
from controleur.composant.LecteurControleur import LecteurControleur
from modele.lecteur.Chanson import Chanson
from modele.lecteur.JukeBoxModele import JukeBoxModele, Ecran
from modele.lecteur.ListeLectureModele import ListeLectureModele
from service.lecteur.VlcService import VlcService
from service.lecteur.YoutubeService import YoutubeService


class YoutubeRechercheControleur(AbstractControleur):
    __vlc_service = inject.attr(VlcService)
    __notificateur_evenement = inject.attr(Observable)

    __youtube_service: YoutubeService
    __liste_lecture_modele: ListeLectureModele
    __lecteur_controleur: LecteurControleur
    __jukebox_modele: JukeBoxModele

    def __init__(self, controleurs_pouvant_gerer_touche: dict[str, PeutGererTouche], modeles: dict[str, object]):
        super().__init__(controleurs_pouvant_gerer_touche, modeles)
        logging.debug("Initialisation du controleur de recherche")
        # noinspection PyTypeChecker
        self.__liste_lecture_modele = modeles["liste_lecture"]
        # noinspection PyTypeChecker
        self.__lecteur_controleur = controleurs_pouvant_gerer_touche["lecteur"]
        # noinspection PyTypeChecker
        self.__jukebox_modele = modeles["jukebox"]

        self.__youtube_service = YoutubeService(self.__vlc_service)
        self.__lecteur_controleur.definir_lecteur_service(self.__youtube_service)

    def lancer(self):
        super().lancer()

    def rechercher_et_jouer_chanson(self, titre_chanson_a_chercher: str):

        chanson = self.__rechercher_chanson(titre_chanson_a_chercher)
        if chanson is None:
            logging.info(f"Pas de chanson trouvée pour le recherche: {titre_chanson_a_chercher}")
            return

        self.__liste_lecture_modele.inserer_puis_jouer_chanson(chanson, self.__youtube_service)
        logging.info(self.__liste_lecture_modele)

    def rechercher_et_ajouter_chanson(self, titre_chanson_a_chercher: str) -> bool:

        chanson = self.__rechercher_chanson(titre_chanson_a_chercher)
        if chanson is None:
            logging.info(f"Pas de chanson trouvée pour le recherche: {titre_chanson_a_chercher}")
            self.__notificateur_evenement.notify(JukeBoxModele.EVENEMENT_NOTIFICATION, "Chanson non trouvée")
            return False

        self.__liste_lecture_modele.ajouter_chanson(chanson)
        self.__notificateur_evenement.notify(JukeBoxModele.EVENEMENT_NOTIFICATION, "Chanson ajoutée à la liste")
        logging.info(self.__liste_lecture_modele)
        return True

    def __rechercher_chanson(self, titre_chanson_a_chercher: str) -> Optional[Chanson]:
        logging.info(f"Lancement de la recherche {titre_chanson_a_chercher}")
        chansons = self.__youtube_service.rechercher_chanson(titre_chanson_a_chercher)

        if chansons is None or len(chansons) == 0:
            logging.info(f"Chanson non trouvée: {titre_chanson_a_chercher}")
            return None

        logging.info(f"Chanson trouvée: {chansons[0]}")
        return chansons[0]

    def _gere_touche(self, touche: Sequence) -> Optional[bool]:
        if touche.egale(ENVOI):
            self.__jukebox_modele.ecran_demande = Ecran.ECRAN_VISUALISATION
            return True
        if touche.egale(ENTREE):
            return False
        return None
