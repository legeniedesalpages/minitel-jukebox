__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-06-18"
__version__ = "1.0.0"

import logging

import inject
from minitel.Minitel import Minitel
from minitel.Sequence import Sequence
from pyobservable import Observable

from controleur.commun.AbstractControleur import AbstractControleur
from controleur.recherche.BibliothequeSpotifyControleur import BibliothequeSpotifyControleur
from modele.lecteur.BibliothequeSpotify import BibliothequeSpotify
from modele.lecteur.BibliothequeSpotifyModele import BibliothequeSpotifyModele
from service.minitel.MinitelExtension import MinitelExtension
from vue.bidule.Liste import Liste
from vue.commun.AbstractEcran import AbstractEcran


class EcranBibliothequeSpotify(AbstractEcran):
    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)
    __notificateur_evenement = inject.attr(Observable)

    __bibliotheque_spotify_modele: BibliothequeSpotifyModele
    __bibliotheque_spotify_controleur: BibliothequeSpotifyControleur

    def __init__(self, controleur: BibliothequeSpotifyControleur, modeles: dict[str, object]):
        super().__init__(controleur, modeles)

        # noinspection PyTypeChecker
        self.__bibliotheque_spotify_modele = modeles["spotify"]
        self.__bibliotheque_spotify_controleur = controleur

    def _affichage_initial(self):
        logging.debug("Affichage initial de l'ecran de la bibliothèque Spotify")
        liste_bibliotheque = self.__bibliotheque_spotify_modele.liste_bibliotheque

        self.__liste = Liste(liste_bibliotheque, self.rendu_element,
                             callback_envoi=self._evenement_selection_par_envoi,
                             callback_entree=self._evenement_selection_par_entree,
                             hauteur_rendu=1, posy_debut=3, posy_fin=24)

        self.__minitel.curseur(False)
        self.__liste.affichage()

    def _get_titre_ecran(self) -> str:
        return "Bibliothèque Spotify"

    def rendu_element(self, element: BibliothequeSpotify, selection: bool, index: int):
        self.__minitel_extension.envoyer_ligne(texte=f"{element.nom_bibliotheque}({str(element.nombre_titre_dedans)})", inversion=selection, couleur="blanc")

    def _evenement_selection_par_envoi(self, element_spotify: BibliothequeSpotify):
        self.__bibliotheque_spotify_controleur.selectionner_hasard_bibliotheque(element_spotify)

    def _evenement_selection_par_entree(self, element_spotify: BibliothequeSpotify):
        self.__bibliotheque_spotify_controleur.selectionner_ordre_bibliotheque(element_spotify)

    def fermer(self):
        pass

    def _get_callback_curseur(self):
        pass

    def _gere_touche(self, touche: Sequence) -> bool:
        if self.__liste.gere_touche(touche):
            return True
        return False
