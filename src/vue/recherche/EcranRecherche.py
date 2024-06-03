__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from minitel.Sequence import Sequence
from minitel.constantes import ENVOI, ENTREE
from minitel.ui.ChampTexte import ChampTexte
from minitel.ui.Label import Label

from controleur.recherche.YoutubeRechercheControleur import YoutubeRechercheControleur
from vue.AbstractEcran import AbstractEcran


class EcranRecherche(AbstractEcran):
    __champ_saisie: ChampTexte
    __recherche_controleur: YoutubeRechercheControleur

    def __init__(self, recherche_controleur: YoutubeRechercheControleur, modeles: dict[str, object]):
        super().__init__(recherche_controleur, modeles)
        self.__recherche_controleur = recherche_controleur
        logging.debug(f"Initialisation de l'écran de recherche {self._minitel}")
        self.__champ_saisie = ChampTexte(self._minitel, 9, 3, 29, 60, "")

    def _affichage_initial(self):
        logging.info("Affichage de l'écran de recherche")
        Label(self._minitel, 1, 3, "Chanson:", "vert").affiche()
        self.__champ_saisie.affiche()

    def _gere_touche(self, touche: Sequence) -> bool:
        if self.__champ_saisie.gere_touche(touche):
            return True

        elif touche.egale(ENVOI):
            self.__recherche_controleur.rechercher_et_jouer_chanson(self.__champ_saisie.valeur)
            return False

        elif touche.egale(ENTREE):
            self.__recherche_controleur.rechercher_et_ajouter_chanson(self.__champ_saisie.valeur)
            return False

        return False

    def _get_titre_ecran(self) -> str:
        return "Recherche ^YOUTUBE^"

    def _get_callback_curseur(self):
        self._minitel.position(
            self.__champ_saisie.posx + self.__champ_saisie.curseur_x - self.__champ_saisie.decalage,
            self.__champ_saisie.posy
        )
        self._minitel.curseur(True)

    def fermer(self):
        logging.info("Fermeture de l'écran de recherche")
