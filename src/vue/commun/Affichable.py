__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-29"
__version__ = "1.0.0"

import abc


class Affichable:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def afficher(self):
        pass

    @abc.abstractmethod
    def fermer(self):
        pass
