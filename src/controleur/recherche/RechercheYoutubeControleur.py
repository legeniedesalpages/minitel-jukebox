__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
import pafy
import vlc

from controleur.recherche.AbstractRechercheControleur import AbstractRechercheControleur
from modele.Chanson import Chanson
from modele.JukeBoxModele import JukeBoxModele
from modele.recherche.AbstractRechercheModele import AbstractRechercheModele
from service.youtube.ChansonService import ChansonService


class RechercheYoutubeControleur(AbstractRechercheControleur):

    def __init__(self, juke_box_modele: JukeBoxModele, recherche_modele: AbstractRechercheModele):
        super().__init__(juke_box_modele, recherche_modele)
        self.__chanson_service = ChansonService()
        self.__player = vlc.MediaPlayer()

    def lancer_recherche(self, titre_chanson, nombre_a_cherche=20):
        logging.debug(f"Lancer la recherche {self.__chanson_service}")
        liste_chanson_trouvee = self.__chanson_service.rechercher_chanson(str(titre_chanson), nombre_a_cherche)
        self._recherche_modele.changer_liste_resultat(liste_chanson_trouvee)

    def _envoyer_lecture(self, chanson: Chanson):
        logging.debug(f"element {chanson}")
        self.__player.stop()
        video = pafy.new(chanson.url_stream)
        best = video.getbestaudio()
        logging.debug(f"best {best}")
        self.__player = vlc.MediaPlayer(best.url)
        self.__player.play()
