__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import inject

from vue.SplashScreenEcran import SplashScreenEcran


class SplashScreenControleur:

    @inject.autoparams()
    def __init__(self, spash_screen_ecran: SplashScreenEcran):
        self.__splash_screen_ecran = spash_screen_ecran

    def afficher_splash_screen(self):
        self.__splash_screen_ecran.afficher()
