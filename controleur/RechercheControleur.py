__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import inject
from minitel.Minitel import Minitel

from controleur.JukeBoxControleur import JukeBoxControleur
from ecran.RechercheEcran import RechercheEcran
from modele.AudioModele import AudioModele


class RechercheControleur(JukeBoxControleur):

    @inject.autoparams()
    def __init__(self, minitel: Minitel, audio_modele: AudioModele):
        super().__init__(audio_modele)
        self.__recherche_ecran = RechercheEcran(minitel, self)

    def afficher_ecran_recherche(self):
        self.__recherche_ecran.afficher()
