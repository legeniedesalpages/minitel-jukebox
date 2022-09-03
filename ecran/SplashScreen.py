__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from time import sleep

import inject
from PIL import Image
from minitel.ImageMinitel import ImageMinitel
from minitel.Minitel import Minitel


class SplashScreen:

    @inject.autoparams()
    def __init__(self, minitel: Minitel):
        self.minitel = minitel

    def afficher(self):
        image = Image.open("ressources/splash.jpg")
        image = image.resize((65, 65), Image.ANTIALIAS)
        image_minitel = ImageMinitel(self.minitel)
        image_minitel.importer(image)
        image_minitel.envoyer(4, 1)

        self.minitel.position(5, 23)
        self.minitel.taille(largeur=2, hauteur=2)
        self.minitel.couleur(caractere='blanc')
        self.minitel.envoyer('Minitel JukeBox')

        self.minitel.sortie.join()
        sleep(2)
        self.minitel.efface()
