__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject

from configuration.MVCCreateur import MVCCreateur
from controleur.TestControleur import TestControleur
from modele.TestModele import TestModele
from vue.EcranDemarrageVue import EcranDemarrageVue
from vue.TestVue import TestVue


class JukeBoxControleur:

    def __init__(self):
        logging.debug("Initialisation du JukeBox")

    def demarrer(self):
        logging.info(f"Démarrage du JukeBox")
        c = MVCCreateur()
        controleur, vue = c.creation(TestControleur, TestVue, [TestModele()])
        print(controleur)
        print(vue)
        EcranDemarrageVue().afficher()


    def fermer(self):
        logging.info(f"Fermeture du JukeBox")
