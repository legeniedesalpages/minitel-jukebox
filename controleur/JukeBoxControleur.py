__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject

from vue.RechercheEcran import RechercheEcran
from vue.SplashScreenEcran import SplashScreenEcran


class JukeBoxService:

    @inject.autoparams()
    def __init__(self, spash_screen_ecran: SplashScreenEcran, recherche_ecran: RechercheEcran):
        logging.info("Initialisation du JukeBox")
        self.__spash_screen_ecran = spash_screen_ecran
        self.__recherche_ecran = recherche_ecran

    def demarrer(self):
        logging.info(f"Démarrage du JukeBox")
        self.__spash_screen_ecran.afficher()

        while True:
            logging.info(f"Affichage de l'écran de recherche")
            self.__recherche_ecran.afficher()
