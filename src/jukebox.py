__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import configparser
import logging

import inject
from minitel.Minitel import Minitel
from pyobservable import Observable

from configuration.EvenementConfiguration import produire_notificateur_evenement
from controleur.commun.JukeBoxControleur import JukeBoxControleur
from controleur.composant.LecteurControleur import LecteurControleur
from modele.lecteur.ListeLectureModele import ListeLectureModele
from service.lecteur.GeminiService import GeminiService
from service.lecteur.SpotifyService import SpotifyService
from service.lecteur.VlcService import VlcService
from service.lecteur.YoutubeService import YoutubeService
from service.minitel.MinitelConfiguration import produire_minitel


def jukebox_inject_config(binder):
    logging.info("Lecture du fichier de properties")
    config = configparser.ConfigParser()
    config.read('ressources/jukebox.ini')

    logging.debug("Configuration de l'injecteur de dépendance")
    binder.bind(Minitel, produire_minitel())
    notificateur_evenement = produire_notificateur_evenement()
    binder.bind(Observable, notificateur_evenement)
    liste_lecture_modele = ListeLectureModele(notificateur_evenement)
    binder.bind(ListeLectureModele, liste_lecture_modele)
    spotify_service = SpotifyService(
        client_id=config.get("spotify", "client_id"),
        client_secret=config.get("spotify", "client_secret"),
        user_id=config.get("spotify", "user_id")
    )
    binder.bind(SpotifyService, spotify_service)
    lecteur_controleur = LecteurControleur(liste_lecture_modele, spotify_service)
    binder.bind(LecteurControleur, lecteur_controleur)

    vlc_service = VlcService(lecteur_controleur)
    binder.bind(VlcService, vlc_service)

    youtube_service = YoutubeService(vlc_service)
    binder.bind(YoutubeService, youtube_service)
    lecteur_controleur.set_youtube_service(youtube_service)

    gemini_service = GeminiService(api_key=config.get("gemini", "api_key"))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)-5s] %(filename)s:%(lineno)d -> %(message)s"
    )

    logging.info("Lancement du Jukebox Minitel")
    inject.configure(jukebox_inject_config)

    juke_box = JukeBoxControleur()
    try:
        juke_box.demarrer()
    except KeyboardInterrupt:
        juke_box.fermer()
        pass

    logging.info("Arret du Jukebox Minitel")
