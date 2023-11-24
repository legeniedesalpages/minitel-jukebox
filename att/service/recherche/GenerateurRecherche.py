__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from controleur.recherche.AbstractRechercheControleur import AbstractRechercheControleur
from controleur.recherche.RechercheYoutubeControleur import RechercheYoutubeControleur
from modele.JukeBoxModele import TypeRecherche, JukeBoxModele
from modele.recherche.AbstractRechercheModele import AbstractRechercheModele
from vue.recherche.RechercheSpotifyVue import RechercheSpotifyVue
from vue.recherche.RechercheYoutubeVue import RechercheYoutubeVue


class GenerateurRecherche:

    def generer(self, juke_box_modele: JukeBoxModele) -> AbstractRechercheControleur:
        if juke_box_modele.type_recherche == TypeRecherche.YOUTUBE:
            return self.__fabriquer_recherche_youtube(juke_box_modele)
        elif juke_box_modele.type_recherche == TypeRecherche.SPOTIFY:
            return self.__fabriquer_recherche_spotify(juke_box_modele)
        else:
            raise Exception(f"Type de recherche {juke_box_modele.type_recherche} inconnu")

    @staticmethod
    def __fabriquer_recherche_youtube(juke_box_modele: JukeBoxModele) -> AbstractRechercheControleur:
        recherche_modele = AbstractRechercheModele()
        recherche_controleur = RechercheYoutubeControleur(juke_box_modele, recherche_modele)
        recherche_vue = RechercheYoutubeVue(recherche_controleur, recherche_modele)
        recherche_controleur.enregistrer_vue(recherche_vue)
        return recherche_controleur

    @staticmethod
    def __fabriquer_recherche_spotify(juke_box_modele: JukeBoxModele) -> AbstractRechercheControleur:
        recherche_modele = AbstractRechercheModele()
        recherche_controleur = AbstractRechercheControleur(juke_box_modele, recherche_modele)
        recherche_vue = RechercheSpotifyVue(recherche_controleur, recherche_modele)
        recherche_controleur.enregistrer_vue(recherche_vue)
        return recherche_controleur
