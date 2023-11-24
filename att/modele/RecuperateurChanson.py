__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from modele.Chanson import Chanson


class RecuperateurChanson:

    def __init__(self):
        logging.info("Initialisation du récupérateur de chanson")

    def suivante(self) -> Chanson:
        return Chanson("1", "un", "01:00", "http://image")
