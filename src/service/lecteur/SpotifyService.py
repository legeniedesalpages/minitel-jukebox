__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import base64
import logging
from typing import List

import requests

from modele.lecteur.BibliothequeSpotify import BibliothequeSpotify
from modele.lecteur.Chanson import Chanson
from service.lecteur.PeutSuggererUneChanson import PeutSuggererUneChanson


class SpotifyService(PeutSuggererUneChanson):
    __CLIENT_ID_SPOTIFY: str
    __CLIENT_SECRET_SPOTIFY: str
    __USER_ID: str

    def __init__(self, client_id: str, client_secret: str, user_id: str):
        logging.info("Initialisation wrapper youtube")
        self.__CLIENT_ID_SPOTIFY = client_id
        self.__CLIENT_SECRET_SPOTIFY = client_secret
        self.__USER_ID = user_id
        self.__auth_token_spotify = self.__spotify_auht_token()
        logging.debug(f"Jeton d'authentification spotify: {self.__auth_token_spotify}")

    def suggestion(self, titre_chanson: str) -> str:
        logging.debug(f"Recherche du track id de la chanson: {titre_chanson}")
        # recherche la chanson à partir de laquelle faire une recommandation
        res = self.__appel_spotify(f"https://api.spotify.com/v1/search?q={titre_chanson}&type=track&market=FR&limit=1")
        track_id = res.json()["tracks"]["items"][0]["id"]
        logging.debug(f"Track id de la chanson {titre_chanson} => {track_id}")

        # recherche la chanson recommandée
        url_recommandation = f"https://api.spotify.com/v1/recommendations?limit=1&market=FR&seed_tracks={track_id}"
        recommandation = self.__appel_spotify(url_recommandation)
        tracks = recommandation.json()["tracks"][0]

        return tracks["artists"][0]["name"] + " - " + tracks["name"]

    def liste_bibliotheque(self) -> List[BibliothequeSpotify]:
        resultat = self.__appel_spotify(f"https://api.spotify.com/v1/users/{self.__USER_ID}/playlists")
        listes_lecture: List[BibliothequeSpotify] = []
        for liste_lecture in resultat.json()["items"]:
            listes_lecture.append(BibliothequeSpotify(liste_lecture["id"], liste_lecture["name"], liste_lecture["tracks"]["total"]))
        return listes_lecture

    def liste_chansons_bibliotheque(self, bibliotheque: BibliothequeSpotify) -> List[Chanson]:
        resultat = self.__appel_spotify(f"https://api.spotify.com/v1/playlists/{bibliotheque.identifiant}/tracks")
        liste_chansons: List[Chanson] = []
        for chanson in resultat.json()["items"]:
            liste_chansons.append(Chanson(titre=f"{chanson['track']['name']} - {chanson['track']['artists'][0]['name']}"))
        return liste_chansons

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
