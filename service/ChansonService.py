__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import base64
import logging
from typing import List

import requests
from youtubesearchpython import VideosSearch

from modele.Chanson import Chanson


class ChansonService:
    __CLIENT_ID_SPOTIFY = "0372daea8b3a496ab5c2ec4dc6e2bd8a"
    __CLIENT_SECRET_SPOTIFY = "220ef945caf54c05817f6feab1315774"

    def __init__(self):
        logging.info("Initialisation wrapper youtube")
        self.__auth_token_spotify = self.__spotify_auht_token()

    @staticmethod
    def rechercher_chanson(chanson_a_chercher: str, nombre: int) -> List[Chanson]:
        logging.info(f"Lancement de la recherche {chanson_a_chercher}")
        resultat_json = VideosSearch(chanson_a_chercher, limit=nombre).result()['result']

        logging.debug(f"Nombre de résultat trouvé: {len(resultat_json)}")

        retour = []
        for resultat in resultat_json:
            retour.append(Chanson(
                resultat['id'],
                resultat['title'],
                resultat['duration'],
                resultat["thumbnails"][0]["url"].split("?", 1)[0],
            ))
        return retour

    def suggestion(self, titre_chanson: str) -> str:
        headers = self.__recuperer_header()

        logging.debug(f"Recherche du track id de la chanson: {titre_chanson}")
        # recherche la chanson a partir de laquelle faire une recommandation
        url_recherche = f"https://api.spotify.com/v1/search?q={titre_chanson}&type=track&market=FR&limit=1"
        res = requests.get(url=url_recherche, headers=headers)
        track_id = res.json()["tracks"]["items"][0]["id"]
        logging.debug(f"Track id de la chanson {titre_chanson} => {track_id}")

        # recherche la chanson recommandée
        url_recommandation = f"https://api.spotify.com/v1/recommendations?limit=1&market=FR&seed_tracks={track_id}"
        recommandation = requests.get(url=url_recommandation, headers=headers)
        tracks = recommandation.json()["tracks"][0]

        return tracks["artists"][0]["name"] + " - " + tracks["name"]

    def __recuperer_header(self):
        return {
            "Authorization": "Bearer " + self.__auth_token_spotify,
            "Accept": "application/json",
            "Content-Type": "application/json"

        }

    @staticmethod
    def __spotify_auht_token():
        url = "https://accounts.spotify.com/api/token"
        headers = {}
        data = {}

        authorisation_base64 = base64.b64encode(
            f"{ChansonService.__CLIENT_ID_SPOTIFY}:{ChansonService.__CLIENT_SECRET_SPOTIFY}".encode('ascii')).decode(
            'ascii')

        headers['Authorization'] = f"Basic {authorisation_base64}"
        data['grant_type'] = "client_credentials"

        requete_auth_token_spotify = requests.post(url, headers=headers, data=data)
        auth_token = requete_auth_token_spotify.json()['access_token']
        logging.debug(f"Token d'authorisation Spotify : {auth_token}")

        return auth_token
