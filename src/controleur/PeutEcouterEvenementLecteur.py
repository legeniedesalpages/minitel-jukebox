__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import abc


class PeutEcouterEvenementLecteur:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def evenement_progression_chanson(self, progression: int):
        pass

    @abc.abstractmethod
    def evenement_fin_chanson(self):
        pass
