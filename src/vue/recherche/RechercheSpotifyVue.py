__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from controleur.recherche.AbstractRechercheControleur import AbstractRechercheControleur
from modele.recherche.AbstractRechercheModele import AbstractRechercheModele
from vue.bidule.Etiquette import Etiquette, Alignement
from vue.recherche.AbstractRechercheVue import AbstractRechercheVue


class RechercheSpotifyVue(AbstractRechercheVue):

    def __init__(self, recherche_controleur: AbstractRechercheControleur, recherche_modele: AbstractRechercheModele):
        super().__init__(recherche_controleur, recherche_modele)

        self._conteneur.ajoute(
            Etiquette.aligne(Alignement.CENTRE, 1, "Recherche dans les services ^Spotify^", "blanc"))
        self._minitel_extension.separateur(2, "rouge")
        self._minitel.curseur(False)
