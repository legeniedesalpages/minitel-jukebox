__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject

from controleur.RechercheControleur import RechercheControleur
from controleur.SplashScreenControleur import SplashScreenControleur
from vue.RechercheEcran import RechercheEcran


class JukeBoxService:

    @inject.autoparams()
    def __init__(self, splash_screen_controleur: SplashScreenControleur, recherche_controleur: RechercheControleur, recherche_ecran: RechercheEcran):
        logging.info("Initialisation du JukeBox")
        self.__splash_screen_controleur = splash_screen_controleur
        self.__recherche_controleur = recherche_controleur
        self.__recherche_ecran = recherche_ecran

    def demarrer(self):
        logging.info(f"Démarrage du JukeBox")
        self.__splash_screen_controleur.afficher_splash_screen()

        while True:
            self.__recherche_controleur.afficher_ecran_recherche()

