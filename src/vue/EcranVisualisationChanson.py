__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
from minitel.Minitel import Minitel

from modele.JukeBoxModele import EvenementSortieEcran
from vue.EcranInterface import EcranInterface


class EcranVisualisationChanson(EcranInterface):
    __minitel = inject.attr(Minitel)

    def afficher(self) -> EvenementSortieEcran:
        logging.info("Affiche visualisation de la chanson")
        self.__minitel.efface('vraimenttout')
        self.__minitel.position(10, 10)
        self.__minitel.envoyer("Chanson...")

        self.__minitel.recevoir_sequence(bloque=True, attente=None)

        logging.info("Ferme la visualisation de la chanson")
        self.__minitel.efface('vraimenttout')

        return EvenementSortieEcran.AFFICHER_RECHERCHE
