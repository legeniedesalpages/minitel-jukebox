__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-31"
__version__ = "1.0.0"

import logging
from typing import List

import inject
from pyobservable import Observable
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

from modele.lecteur.Chanson import Chanson
from modele.lecteur.JukeBoxModele import JukeBoxModele
from service.lecteur.AbstractLecteurService import AbstractLecteurService
from service.lecteur.VlcService import VlcService


class YoutubeService(AbstractLecteurService):

    __notificateur_evenement = inject.attr(Observable)

    def __init__(self, vlc_service: VlcService):
        super().__init__(vlc_service)

    @staticmethod
    def rechercher_chanson(chanson_a_chercher: str, nombre: int = 1) -> List[Chanson]:
        logging.info(f"Lancement de la recherche {chanson_a_chercher}")
        resultat_json = VideosSearch(chanson_a_chercher, limit=nombre).result()['result']

        logging.debug(f"Nombre de résultat trouvé: {len(resultat_json)}")

        retour = []
        for resultat in resultat_json:
            # noinspection PyTypeChecker
            retour.append(Chanson(
                resultat['id'],
                resultat['title'],
                resultat['duration'],
                resultat["thumbnails"][0]["url"].split("?", 1)[0],
            ))
        return retour

    def preparer_chanson(self, chanson: Chanson):
        if chanson.identifiant_video is None:
            chanson_trouve = self.rechercher_chanson(chanson.titre, 1)
            logging.debug(f"Complete info chanson: {chanson_trouve}")
            chanson.identifiant_video = chanson_trouve[0].identifiant_video
            chanson.url_image = chanson_trouve[0].url_image
            chanson.duree = chanson_trouve[0].duree
            chanson.set_url_stream()

    def jouer(self, chanson: Chanson):
        logging.debug(f"YDL, tentative de récupération chanson: {chanson}")
        if chanson.identifiant_video is None:
            chanson_trouve = self.rechercher_chanson(chanson.titre, 1)
            logging.debug(f"Complete info chanson: {chanson_trouve}")
            chanson.identifiant_video = chanson_trouve[0].identifiant_video
            chanson.url_image = chanson_trouve[0].url_image
            chanson.duree = chanson_trouve[0].duree
            chanson.set_url_stream()

        ydl_opts = {
            "socket_timeout": 15,
            "retries": 1,
            "format": "bestaudio[ext=m4a]/bestaudio/best",  # fallback progressif
            "extractor_args": {
                "youtube": {"player_client": ["android", "mweb", "web"]}
            },
            "cookiefile": "/home/pi/cookies.txt",  # ou firefox
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(chanson.url_stream, download=False)
            self._vlc_service.jouer(info['url'])
