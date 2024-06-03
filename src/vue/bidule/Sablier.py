__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
import threading
import time

import inject
from minitel.Minitel import Minitel

from service.minitel.MinitelExtension import MinitelExtension


class Sablier:
    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)

    __sablier_tourne: bool

    def __init__(self):
        self.__evenement = threading.Event()
        self.__compteur = 0
        self.__fin = False
        threading.Thread(target=self._dessine).start()
        self.__sablier_tourne = False

    def detruire(self):
        logging.debug("Fin du thread du sablier")
        self.__fin = True
        self.__evenement.set()
        self.__sablier_tourne = False

    def demarrer(self):
        logging.debug("Affichage du sablier")
        self.__evenement.set()
        self.__sablier_tourne = True

    def arreter(self) -> bool:
        logging.debug("Effacement du sablier")
        etat_avant = self.__sablier_tourne
        self.__evenement.clear()
        self.__minitel.position(39, 1)
        self.__minitel.envoyer(" ")
        self.__sablier_tourne = False
        return etat_avant

    def _dessine(self):
        while not self.__fin:
            self.__minitel.curseur(False)
            self.__compteur += 1
            self.__minitel.position(39, 1)
            self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()
            self.__minitel.envoyer(str(self.__compteur % 6))
            self.__minitel_extension.revenir_jeu_caractere_standard()
            time.sleep(80 / 1000)
            self.__evenement.wait()
