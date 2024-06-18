__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-06-13"
__version__ = "1.0.0"

import logging

import inject
from minitel.Minitel import Minitel
from minitel.Sequence import Sequence
from pyobservable import Observable

from controleur.commun.AbstractControleur import AbstractControleur
from modele.lecteur.Chanson import Chanson
from modele.lecteur.ListeLectureModele import ListeLectureModele
from service.lecteur.VlcService import VlcService
from service.lecteur.YoutubeService import YoutubeService
from service.minitel.MinitelExtension import MinitelExtension
from vue.bidule.Liste import Liste
from vue.commun.AbstractEcran import AbstractEcran


class EcranListeLecture(AbstractEcran):
    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)
    __notificateur_evenement = inject.attr(Observable)
    __vlc_service = inject.attr(VlcService)

    __liste_lecture_modele: ListeLectureModele

    def __init__(self, controleur: AbstractControleur, modeles: dict[str, object]):
        super().__init__(controleur, modeles)
        logging.debug("Visualisation liste de lecture vue init")
        # noinspection PyTypeChecker
        self.__liste_lecture_modele = modeles["liste_lecture"]
        self.__youtube_service = YoutubeService(self.__vlc_service)
        self.__liste = Liste(self.__liste_lecture_modele.liste_lecture, self.rendu_element,
                             callback_envoi=self._evenement_selection_par_envoi,
                             callback_entree=self._evenement_selection_par_entree,
                             hauteur_rendu=1, posy_debut=3, posy_fin=24)

    def _affichage_initial(self):
        logging.debug("Affichage initial de l'ecran de la liste de lecture")
        self.__minitel.curseur(False)
        self.__liste.affichage()

    def _get_titre_ecran(self) -> str:
        return "Liste de lecture"

    def _get_callback_curseur(self):
        pass

    def _evenement_selection_par_envoi(self, chanson: Chanson):
        logging.debug(f"Evenement selection par envoi: {chanson}")
        self.__liste_lecture_modele.jouer_chanson_a_index(self.__liste_lecture_modele.liste_lecture.index(chanson), self.__youtube_service)

    def _evenement_selection_par_entree(self, chanson: Chanson):
        logging.debug(f"Evenement selection par entree: {chanson}")
        self.__liste_lecture_modele.jouer_chanson_a_index(self.__liste_lecture_modele.liste_lecture.index(chanson), self.__youtube_service)

    def _gere_touche(self, touche: Sequence) -> bool:
        if self.__liste.gere_touche(touche):
            return True
        return False

    def fermer(self):
        pass

    def rendu_element(self, element: Chanson, selection: bool, index: int):
        i = self.__liste_lecture_modele.liste_lecture.index(element)
        logging.debug(f"Rendu element: {i} {self.__liste_lecture_modele.index_courant}")
        if i < self.__liste_lecture_modele.index_courant:
            couleur = 1
        elif i == self.__liste_lecture_modele.index_courant:
            couleur = "blanc"
        else:
            couleur = 5
        self.__minitel_extension.envoyer_ligne(texte=f"{element.titre}", inversion=selection, couleur=couleur)
