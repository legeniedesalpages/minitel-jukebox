__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import pafy
import vlc
from youtubesearchpython import VideosSearch


class LecteurService:

    def __init__(self):
        logging.info("Initialisation wrapper youtube")
        self.__player = None

    def rechercher_chanson(self, texte_a_chercher, nombre: int) -> []:
        logging.info(f"Lancement de la recherche {texte_a_chercher}")
        resultat_json = VideosSearch(texte_a_chercher, limit=nombre).result()['result']
        retour = []
        for resultat in resultat_json:
            thumb = resultat['thumbnails'][0]

            retour.append({
                "titre": resultat['title'],
                "url": resultat['link'],
                "duree": resultat['duration'],
                "image_url": thumb['url'].split("?", 1)[0],
                "image_x": thumb['width'],
                "image_y": thumb['height'],
            })
        return retour

    def jouer_url(self, url):
        audio = pafy.new(url)
        best = audio.getbestaudio()
        if self.__player is not None:
            self.__player.stop()
        self.__player = vlc.MediaPlayer(best.url)
        self.__player.play()

    def pause_ou_reprendre(self):
        if self.__player is None:
            logging.debug("Pas de chanson")
            return None
        elif self.__player.is_playing():
            logging.debug("La lecture était en cours, on met en pause")
            self.__player.pause()
            return False
        else:
            logging.debug("La lecture était en pause, on reprend")
            self.__player.play()
            return True
