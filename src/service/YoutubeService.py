__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-31"
__version__ = "1.0.0"

import logging
from typing import List

from pafy import pafy
from youtubesearchpython import VideosSearch

from modele.Chanson import Chanson
from service.AbstractLecteurService import AbstractLecteurService
from service.VlcService import VlcService


class YoutubeService(AbstractLecteurService):

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

    def jouer(self, chanson: Chanson):
        video = pafy.new(chanson.url_stream)
        best = video.getbestaudio()
        self._vlc_service.jouer(best.url)
