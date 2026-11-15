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


class SpotifyAPIError(Exception):
    pass


class SpotifyService(PeutSuggererUneChanson):
    __CLIENT_ID_SPOTIFY: str
    __CLIENT_SECRET_SPOTIFY: str
    __USER_ID: str

    def __init__(self, client_id: str, client_secret: str, user_id: str):
        logging.info("Initialisation wrapper youtube")
        self.__CLIENT_ID_SPOTIFY = client_id
        self.__CLIENT_SECRET_SPOTIFY = client_secret
        self.__USER_ID = user_id
        self.__erreur_initialisation = None
        try:
            self.__auth_token_spotify = self.__spotify_auht_token()
        except SpotifyAPIError as error:
            self.__auth_token_spotify = None
            self.__erreur_initialisation = str(error)
            logging.error("Initialisation Spotify impossible: %s", error)

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
        if self.__erreur_initialisation:
            raise SpotifyAPIError(self.__erreur_initialisation)

        url = f"https://api.spotify.com/v1/users/{self.__USER_ID}/playlists"
        try:
            resultat = self.__appel_spotify(url)
            resultat.raise_for_status()
            elements = resultat.json()["items"]
            return [
                BibliothequeSpotify(item["id"], item["name"], item["tracks"]["total"])
                for item in elements
            ]
        except requests.HTTPError as error:
            response = error.response
            status = response.status_code if response is not None else "inconnu"
            if status == 401:
                message = "Authentification Spotify refusee (HTTP 401)."
            elif status == 403:
                message = "Acces a la bibliotheque Spotify refuse (HTTP 403)."
            elif status == 404:
                message = "Bibliotheque ou utilisateur Spotify introuvable (HTTP 404)."
            elif status == 429:
                message = "Limite Spotify atteinte (HTTP 429). Reessayez plus tard."
            else:
                message = f"Spotify a renvoye une erreur HTTP {status}."
            details = response.text[:500] if response is not None else str(error)
            logging.error("Echec de la requete Spotify (%s): %s", status, details)
            raise SpotifyAPIError(message) from error
        except requests.Timeout as error:
            logging.exception("Delai depasse lors de la recuperation des bibliotheques Spotify")
            raise SpotifyAPIError("Spotify ne repond pas (delai depasse).") from error
        except (ValueError, KeyError, TypeError) as error:
            logging.exception("Reponse invalide lors de la recuperation des bibliotheques Spotify")
            raise SpotifyAPIError("Spotify a renvoye une reponse invalide.") from error
        except requests.RequestException as error:
            logging.exception("Erreur reseau lors de la recuperation des bibliotheques Spotify")
            raise SpotifyAPIError("Spotify est inaccessible (erreur reseau).") from error

    def liste_chansons_bibliotheque(self, bibliotheque: BibliothequeSpotify) -> List[Chanson]:
        resultat = self.__appel_spotify(f"https://api.spotify.com/v1/playlists/{bibliotheque.identifiant}/tracks")
        liste_chansons: List[Chanson] = []
        logging.debug(f"Récupération des chansons de la playlist {resultat.json()}")
        for chanson in resultat.json()["items"]:
            logging.debug(f"Chanson {chanson}")
            if chanson['track'] is not None:
                liste_chansons.append(Chanson(titre=f"{chanson['track']['name']} - {chanson['track']['artists'][0]['name']}"))
        return liste_chansons

    def __appel_spotify(self, url):
        if self.__erreur_initialisation:
            raise SpotifyAPIError(self.__erreur_initialisation)
        headers = {
            "Authorization": "Bearer " + self.__auth_token_spotify,
            "Accept": "application/json",
            "Content-Type": "application/json"

        }
        resultat = requests.get(url=url, headers=headers, timeout=10)
        resultat.raise_for_status()
        return resultat

    def __spotify_auht_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {}
        data = {}

        authorisation_base64 = base64.b64encode(
            f"{self.__CLIENT_ID_SPOTIFY}:{self.__CLIENT_SECRET_SPOTIFY}".encode('ascii')).decode(
            'ascii')

        headers['Authorization'] = f"Basic {authorisation_base64}"
        data['grant_type'] = "client_credentials"

        try:
            requete_auth_token_spotify = requests.post(url, headers=headers, data=data, timeout=10)
            requete_auth_token_spotify.raise_for_status()
            auth_token = requete_auth_token_spotify.json()["access_token"]
        except requests.HTTPError as error:
            response = error.response
            status = response.status_code if response is not None else "inconnu"
            details = response.text[:500] if response is not None else str(error)
            logging.error("Echec de l'authentification Spotify (HTTP %s): %s", status, details)
            raise SpotifyAPIError(f"Authentification Spotify impossible (HTTP {status}).") from error
        except requests.Timeout as error:
            logging.exception("Delai depasse lors de l'authentification Spotify")
            raise SpotifyAPIError("Spotify ne repond pas (delai depasse).") from error
        except (ValueError, KeyError, TypeError) as error:
            logging.exception("Reponse invalide lors de l'authentification Spotify")
            raise SpotifyAPIError("Spotify a renvoye une reponse d'authentification invalide.") from error
        except requests.RequestException as error:
            logging.exception("Erreur reseau lors de l'authentification Spotify")
            raise SpotifyAPIError("Spotify est inaccessible (erreur reseau).") from error

        logging.debug("Jeton d'authentification Spotify obtenu")
        return auth_token
