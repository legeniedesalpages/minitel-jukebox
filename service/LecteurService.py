__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import pafy
import vlc


class LecteurService:
    EVENEMENT_CHARGEMENT = "EvenementChargement"
    EVENEMENT_LECTURE = "EvenementLecture"
    EVENEMENT_PAUSE = "EvenementPause"
    EVENEMENT_AVANCEMENT = "EvenementAvancement"
    EVENEMENT_ARRET = "EvenementArret"
    EVENEMENT_FIN_CHANSON = "EvenementFinChanson"

    def __init__(self):
        logging.info("Initialisation wrapper youtube")
        self.__vlc_instance = vlc.Instance()
        self.__player = self.__vlc_instance.media_player_new()
        self.__attacher_evenement(self.__player)
        self.__callback_evenement = None

    def arreter_lecture(self):
        self.__player.stop()

    def jouer_url(self, url):
        audio = pafy.new(url)
        best = audio.getbestaudio()

        self.__player.set_media(self.__vlc_instance.media_new(best.url))
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

    def __attacher_evenement(self, player):
        event_manager = player.event_manager()
        event_manager.event_attach(vlc.EventType.MediaPlayerOpening, self.evenement_chargement)
        event_manager.event_attach(vlc.EventType.MediaPlayerPlaying, self.evenement_lecture)
        event_manager.event_attach(vlc.EventType.MediaPlayerPaused, self.evenement_pause)
        event_manager.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.evenement_avancement)
        event_manager.event_attach(vlc.EventType.MediaPlayerStopped, self.evenement_arret)
        event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.evenement_fin_chanson_atteinte)

    def enregistrer_callback(self, callback_evenement):
        self.__callback_evenement = callback_evenement

    def oublier_callback(self):
        self.__callback_evenement = None

    def evenement_avancement(self, event: vlc.Event):
        if self.__callback_evenement is not None:
            self.__callback_evenement(LecteurService.EVENEMENT_AVANCEMENT, int(self.__player.get_time() / 1000))

    def evenement_lecture(self, event: vlc.Event):
        if self.__callback_evenement is not None:
            self.__callback_evenement(LecteurService.EVENEMENT_LECTURE, "")

    def evenement_arret(self, event: vlc.Event):
        if self.__callback_evenement is not None:
            self.__callback_evenement(LecteurService.EVENEMENT_ARRET, "")

    def evenement_chargement(self, event: vlc.Event):
        if self.__callback_evenement is not None:
            self.__callback_evenement(LecteurService.EVENEMENT_CHARGEMENT, "")

    def evenement_pause(self, event: vlc.Event):
        if self.__callback_evenement is not None:
            self.__callback_evenement(LecteurService.EVENEMENT_PAUSE, "")

    def evenement_fin_chanson_atteinte(self, event: vlc.Event):
        if self.__callback_evenement is not None:
            self.__callback_evenement(LecteurService.EVENEMENT_FIN_CHANSON, "")
