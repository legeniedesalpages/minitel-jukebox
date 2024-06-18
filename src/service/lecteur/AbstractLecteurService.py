__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-06-01"
__version__ = "1.0.0"

import abc

from modele.lecteur.Chanson import Chanson
from service.lecteur.VlcService import VlcService


class AbstractLecteurService:
    __metaclass__ = abc.ABCMeta

    _vlc_service: VlcService

    def __init__(self, vlc_service: VlcService):
        self._vlc_service = vlc_service

    @abc.abstractmethod
    def jouer(self, chanson: Chanson):
        pass

    def pause(self):
        return self._vlc_service.pause()

    def relance(self):
        return self._vlc_service.relance()

    def arreter(self):
        return self._vlc_service.arreter()

    def avancer(self):
        return self._vlc_service.avancer()

    def reculer(self):
        return self._vlc_service.reculer()
