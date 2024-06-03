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
from minitel.Sequence import Sequence

from controleur.AbstractControleur import AbstractControleur
from modele.Chanson import Chanson
from modele.ListeLectureModele import ListeLectureModele
from vue.AbstractEcran import AbstractEcran


class EcranVisualisation(AbstractEcran):
    __minitel = inject.attr(Minitel)

    __liste_lecture_modele: ListeLectureModele

    def __init__(self, controleur: AbstractControleur, modeles: dict[str, object]):
        super().__init__(controleur, modeles)
        logging.info("Visualisation chanson vue init")
        # noinspection PyTypeChecker
        self.__liste_lecture_modele = modeles["liste_lecture"]

    def _affichage_initial(self):
        self.__minitel.curseur(False)
        self.afficher_chanson(self.__liste_lecture_modele.chanson_courante())

    def _get_titre_ecran(self) -> str:
        if self.__liste_lecture_modele.chanson_courante() is None:
            return "Aucune chanson"
        return self.__liste_lecture_modele.chanson_courante().titre[:30]

    def _get_callback_curseur(self):
        pass

    def _gere_touche(self, touche: Sequence) -> bool:
        return False

    def fermer(self):
        logging.info("Ferme la visualisation de la chanson")
        self.__minitel.efface('vraimenttout')

    def afficher_chanson(self, chanson: Chanson):
        if chanson is None:
            return
        logging.info(f"Affiche visualisation de la chanson {chanson}")
        self.__minitel.curseur(False)

        img_data = requests.get(chanson.url_image).content
        with open('/tmp/image.jpg', 'wb') as handler:
            handler.write(img_data)

        image = Image.open("/tmp/image.jpg")
        image = image.resize((80, 69), Image.ANTIALIAS)
        image_minitel = ImageMinitel(self.__minitel)
        image_minitel.importer(image)
        image_minitel.envoyer(1, 2)
