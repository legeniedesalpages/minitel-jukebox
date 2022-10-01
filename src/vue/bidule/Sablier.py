__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
import threading

import inject
import time
from minitel.Minitel import Minitel

from service.minitel.MinitelExtension import MinitelExtension


class Sablier:
    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)

    def __init__(self):
        self.__evenement = threading.Event()
        self.__compteur = 0
        self.__fin = False
        self.__declencheur = threading.Thread(target=self._dessine)
        self.__declencheur.start()

    def eteindre(self):
        logging.info("Fin du thread du sablier")
        self.__fin = True
        self.__evenement.set()

    def demarrer(self):
        logging.debug("Affichage du sablier")
        self.__evenement.set()

    def arreter(self):
        logging.debug("Effacement du sablier")
        self.__evenement.clear()
        self.__minitel.position(1, 1)
        self.__minitel.envoyer(" ")

    def _dessine(self):
        self.__evenement.wait()
        while not self.__fin:
            self.__minitel.curseur(False)
            self.__compteur += 1
            self.__minitel.position(1, 1)
            self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()
            self.__minitel.envoyer(str(self.__compteur % 6))
            self.__minitel_extension.revenir_jeu_caractere_standard()
            time.sleep(80 / 1000)
            self.__evenement.wait()
