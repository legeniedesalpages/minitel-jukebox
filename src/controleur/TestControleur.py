__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from minitel.Minitel import Minitel

from controleur.AbstractControleur import AbstractControleur
from modele.TestModele import TestModele


class TestControleur(AbstractControleur):

    def __init__(self, minitel: Minitel, test_modele: TestModele):
        super().__init__(minitel, [test_modele])
        logging.info("test controleur ok")
