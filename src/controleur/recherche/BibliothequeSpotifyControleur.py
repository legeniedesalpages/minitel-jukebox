__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-06-18"
__version__ = "1.0.0"

import logging
from typing import Optional

import inject
from minitel.Sequence import Sequence

from controleur.commun.AbstractControleur import AbstractControleur
from controleur.commun.PeutGererTouche import PeutGererTouche
from modele.lecteur.BibliothequeSpotifyModele import BibliothequeSpotifyModele
from modele.lecteur.ListeLectureModele import ListeLectureModele
from service.lecteur.SpotifyService import SpotifyAPIError, SpotifyService
from service.lecteur.VlcService import VlcService
from service.lecteur.YoutubeService import YoutubeService


class BibliothequeSpotifyControleur(AbstractControleur):
    __spotify_service = inject.attr(SpotifyService)
    __vlc_service = inject.attr(VlcService)

    __bibliotheque_spotify_modele: BibliothequeSpotifyModele
    __liste_lecture_modele: ListeLectureModele

    def __init__(self, controleurs_pouvant_gerer_touche: dict[str, PeutGererTouche], modeles: dict[str, object]):
        super().__init__(controleurs_pouvant_gerer_touche, modeles)
        # noinspection PyTypeChecker
        self.__bibliotheque_spotify_modele = modeles["spotify"]
        # noinspection PyTypeChecker
        self.__liste_lecture_modele = modeles["liste_lecture"]

        self.__youtube_service = YoutubeService(self.__vlc_service)

    def lancer(self):
        try:
            self.__bibliotheque_spotify_modele.liste_bibliotheque = self.__spotify_service.liste_bibliotheque()
            self.__bibliotheque_spotify_modele.erreur = None
            logging.info(
                f"Liste des bibliothèques Spotify récupérée: "
                f"{self.__bibliotheque_spotify_modele.liste_bibliotheque}")
        except SpotifyAPIError as error:
            self.__bibliotheque_spotify_modele.liste_bibliotheque = []
            self.__bibliotheque_spotify_modele.erreur = str(error)
            logging.error("Impossible de charger la bibliothèque Spotify: %s", error)
        super().lancer()

    def _gere_touche(self, touche: Sequence) -> Optional[bool]:
        pass

    def selectionner_hasard_bibliotheque(self, bibliotheque):
        logging.info(f"Sélectionne la bibliothèque {bibliotheque} au hasard")
        liste_lecture = self.__spotify_service.liste_chansons_bibliotheque(bibliotheque)
        self.__liste_lecture_modele.ajouter_au_hasard(liste_lecture)
        self.__liste_lecture_modele.jouer_chanson_courante(self.__youtube_service)

    def selectionner_ordre_bibliotheque(self, bibliotheque):
        logging.info(f"Sélectionne la bibliothèque {bibliotheque} au hasard")
        liste_lecture = self.__spotify_service.liste_chansons_bibliotheque(bibliotheque)
        self.__liste_lecture_modele.liste_lecture = liste_lecture
        self.__liste_lecture_modele.index_courant = 0
        self.__liste_lecture_modele.jouer_chanson_courante(self.__youtube_service)
