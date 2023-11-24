__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
import requests
from PIL import Image
from minitel.ImageMinitel import ImageMinitel
from minitel.Minitel import Minitel

from modele.Chanson import Chanson
from modele.JukeBoxModele import EvenementSortieEcran
from vue.EcranInterface import EcranInterface
from vue.composant.AudioComposantVue import AudioComposantVue


class EcranVisualisationChanson(EcranInterface):
    __minitel = inject.attr(Minitel)

    def __init__(self):
        self.__audio_composant = AudioComposantVue(self.__minitel, 40, 3, self._repositionnement_curseur)

    def afficher_chanson(self, chanson: Chanson) -> EvenementSortieEcran:
        logging.info(f"Affiche visualisation de la chanson {chanson}")
        self.__minitel.curseur(False)
        self.__minitel.efface('vraimenttout')

        self.__minitel.position(1, 23)
        self.__minitel.taille(largeur=1, hauteur=2)
        self.__minitel.couleur(caractere='blanc')
        self.__minitel.envoyer(chanson.titre[:39])

        img_data = requests.get(chanson.url_image).content
        with open('/tmp/image.jpg', 'wb') as handler:
            handler.write(img_data)

        image = Image.open("/tmp/image.jpg")
        image = image.resize((80, 65), Image.ANTIALIAS)
        image_minitel = ImageMinitel(self.__minitel)
        image_minitel.importer(image)
        image_minitel.envoyer(1, 1)

        while True:
            sequence = self.__minitel.recevoir_sequence(bloque=True, attente=None)
            if self.gerer_touche(sequence) != EvenementSortieEcran.PAS_DE_SORTIE:
                break

        logging.info("Ferme la visualisation de la chanson")
        self.__minitel.efface('vraimenttout')

        return EvenementSortieEcran.AFFICHER_RECHERCHE

    def gerer_touche(self, sequence) -> EvenementSortieEcran:
        if self.__audio_composant.gere_touche(sequence):
            return EvenementSortieEcran.PAS_DE_SORTIE

    def _repositionnement_curseur(self):
        logging.debug(f"Repositionnement du curseur {self.__audio_composant.posx}")
