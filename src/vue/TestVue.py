__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from minitel.Minitel import Minitel

from controleur.TestControleur import TestControleur
from service.minitel.MinitelExtension import MinitelExtension
from vue.AbstractVue import AbstractVue


class TestVue(AbstractVue):

    def __init__(self, minitel: Minitel, minitel_extension: MinitelExtension, test_controleur: TestControleur,
                 test_modele):
        super().__init__(minitel, minitel_extension, test_controleur, [test_modele])
        logging.info("Test vue init")
