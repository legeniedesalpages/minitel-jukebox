__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-06-02"
__version__ = "1.0.0"

import logging
from typing import Optional

import vlc

from controleur.PeutEcouterEvenementLecteur import PeutEcouterEvenementLecteur


class VlcService:
    __event_manager: vlc.libvlc_media_player_event_manager

    def __init__(self, lecteur_controleur: PeutEcouterEvenementLecteur):
        logging.debug("Initialisation du service VLC")
        self.__player: Optional[vlc.MediaPlayer] = None
        self.__event_manager = None
        self.__lecture_controleur = lecteur_controleur

    def jouer(self, url):
        self.__player = vlc.MediaPlayer(url)
        self.__player.play()
        self.__event_manager = self.__player.event_manager()
        self.__event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self._evenement_fin_chanson)
        self.__event_manager.event_attach(vlc.EventType.MediaPlayerPositionChanged, self._evenement_progression_chanson)

    def arreter(self):
        if self.__event_manager is not None:
            self.__event_manager.event_detach(vlc.EventType.MediaPlayerEndReached)
            self.__event_manager.event_detach(vlc.EventType.MediaPlayerPositionChanged)

        if self.__player is not None:
            self.__player.stop()

    def pause(self):
        if self.__player is not None:
            self.__player.pause()

    def relance(self):
        if self.__player is not None:
            self.__player.play()

    def _evenement_fin_chanson(self, event):
        self.__lecture_controleur.evenement_fin_chanson()

    def _evenement_progression_chanson(self, event):
        self.__lecture_controleur.evenement_progression_chanson(progression=int(100 * self.__player.get_position()))
