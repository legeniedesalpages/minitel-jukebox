__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import base64
import logging

import requests


class SpotifyService:
    __CLIENT_ID_SPOTIFY = "0372daea8b3a496ab5c2ec4dc6e2bd8a"
    __CLIENT_SECRET_SPOTIFY = "220ef945caf54c05817f6feab1315774"
    __USER_ID = "31meuagwwtxgaq7pzvbcpdhozz7u"

    def __init__(self):
        logging.info("Initialisation wrapper youtube")
        self.__auth_token_spotify = self.__spotify_auht_token()
        logging.debug(f"Jeton d'authentification spotify: {self.__auth_token_spotify}")

    def suggestion(self, titre_chanson: str) -> str:
        logging.debug(f"Recherche du track id de la chanson: {titre_chanson}")
        # recherche la chanson a partir de laquelle faire une recommandation
        res = self.__appel_spotify(f"https://api.spotify.com/v1/search?q={titre_chanson}&type=track&market=FR&limit=1")
        track_id = res.json()["tracks"]["items"][0]["id"]
        logging.debug(f"Track id de la chanson {titre_chanson} => {track_id}")

        # recherche la chanson recommandée
        url_recommandation = f"https://api.spotify.com/v1/recommendations?limit=1&market=FR&seed_tracks={track_id}"
        recommandation = self.__appel_spotify(url_recommandation)
        tracks = recommandation.json()["tracks"][0]

        return tracks["artists"][0]["name"] + " - " + tracks["name"]

    def listes_lecture(self):
        resultat = self.__appel_spotify(f"https://api.spotify.com/v1/users/{self.__USER_ID}/playlists")
        listes_lecture = []
        for liste_lecture in resultat.json()["items"]:
            listes_lecture.append(liste_lecture["name"] + ", " + str(liste_lecture["tracks"]["total"]))
        return listes_lecture

    def __appel_spotify(self, url):
        headers = {
            "Authorization": "Bearer " + self.__auth_token_spotify,
            "Accept": "application/json",
            "Content-Type": "application/json"

        }
        return requests.get(url=url, headers=headers)

    def __spotify_auht_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {}
        data = {}

        authorisation_base64 = base64.b64encode(
            f"{self.__CLIENT_ID_SPOTIFY}:{self.__CLIENT_SECRET_SPOTIFY}".encode('ascii')).decode(
            'ascii')

        headers['Authorization'] = f"Basic {authorisation_base64}"
        data['grant_type'] = "client_credentials"

        requete_auth_token_spotify = requests.post(url, headers=headers, data=data)
        resultat = requete_auth_token_spotify.json()
        auth_token = resultat['access_token']
        print(resultat)
        logging.debug(f"Token d'authorisation Spotify : {auth_token}")

        return auth_token
