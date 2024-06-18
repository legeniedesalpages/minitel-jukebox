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


class EcranDemarrage:

    @inject.autoparams()
    def __init__(self, minitel: Minitel):
        self.__minitel = minitel

    def afficher(self):
        self.__minitel.position(5, 23)
        self.__minitel.taille(largeur=2, hauteur=2)
        self.__minitel.couleur(caractere='blanc')
        self.__minitel.envoyer('Minitel JukeBox')

        image = Image.open("/home/pi/minitel/minitel-jukebox/ressources/splash.jpg")
        image = image.resize((65, 65), Image.ANTIALIAS)
        image_minitel = ImageMinitel(self.__minitel)
        image_minitel.importer(image)
        image_minitel.envoyer(4, 1)

        self.__minitel.sortie.join()
        sleep(2)
        self.__minitel.efface('vraimenttout')
