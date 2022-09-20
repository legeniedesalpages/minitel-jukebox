__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from minitel.ui.ChampTexte import ChampTexte
from minitel.ui.Label import Label

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
        self._conteneur.ajoute(Label(self._minitel, 1, 3, "Playlist:", "vert"))
        self._conteneur.ajoute(ChampTexte(self._minitel, 11, 3, 28, 60))
