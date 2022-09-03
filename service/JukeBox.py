__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
from minitel.Minitel import Minitel

from ecran.SplashScreen import SplashScreen


class JukeBox:

    @inject.autoparams()
    def __init__(self, minitel: Minitel):
        logging.info("Initialisation du JukeBox")
        self.minitel = minitel

    def demarrer(self):
        logging.info(f"Démarrage du JukeBox {self.minitel}")
        SplashScreen().afficher()
