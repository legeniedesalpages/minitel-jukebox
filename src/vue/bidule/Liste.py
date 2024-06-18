__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-06-14"
__version__ = "1.0.0"

import logging
from math import floor

import inject
from minitel.Minitel import Minitel
from minitel.Sequence import Sequence
from minitel.constantes import HAUT, BAS, DROITE, GAUCHE, ENVOI, ENTREE
from pyobservable import Observable

from service.minitel.MinitelExtension import MinitelExtension
from vue.bidule.Separateur import Separateur


class Liste:
    EVENEMENT_LISTE_CHANGE_PAGE = "evenementListeChangePage"

    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)
    __notificateur_evenement = inject.attr(Observable)

    __index_ecran: int = -1
    __page_courante: int = 0
    __posy_debut: int
    __posy_fin: int

    __callback_envoi = None
    __callback_entree = None

    def __init__(self, liste_elements, rendu_element, callback_envoi=None, callback_entree=None, hauteur_rendu: int = 1, posy_debut: int = 2, posy_fin: int = 24):
        logging.debug("Initialisation de la liste")
        self.__liste_elements = liste_elements
        self.__rendu_element = rendu_element
        self.__hauteur_rendu = hauteur_rendu
        self.__posy_debut = posy_debut
        self.__posy_fin = posy_fin
        self.__callback_envoi = callback_envoi
        self.__callback_entree = callback_entree

    def affichage(self):
        logging.debug("Affichage de la liste")

        if self.__hauteur_rendu > 0:
            for i in range(self.__max_element_par_page()):
                position_separateur = self.__position_par_index(i + 1) - 1
                Separateur.leger(position_separateur)

        self.__affichage_element()

    def __affichage_element(self):
        taille = min(self.__max_element_par_page(), len(self.__liste_elements) - self.__page_courante * self.__max_element_par_page())
        for i in range(taille):
            self.__minitel.position(1, self.__position_par_index(i))
            self.__rendu_element(self.__liste_elements[self.__index_rapport_page(i)], i == self.__index_ecran, self.__index_rapport_page(i))

        for i in range(taille, self.__max_element_par_page()):
            self.__minitel_extension.effacer_ligne(self.__position_par_index(i))

        if self.__page_courante < 10:
            texte = f" {self.__page_courante + 1}/{self.__nombre_de_page() + 1}"
        else:
            texte = f"{self.__page_courante + 1}/{self.__nombre_de_page() + 1}"
        self.__notificateur_evenement.notify(self.EVENEMENT_LISTE_CHANGE_PAGE, texte)

    def __index_rapport_page(self, index: int) -> int:
        return index + self.__page_courante * self.__max_element_par_page()

    def __position_par_index(self, index: int):
        return self.__posy_debut + (index * (self.__hauteur_rendu + 1))

    def __max_element_par_page(self) -> int:
        return int(floor((self.__posy_fin - self.__posy_debut) / (self.__hauteur_rendu + 1)))

    def __nombre_de_page(self) -> int:
        logging.debug(f"{len(self.__liste_elements)} / {self.__max_element_par_page()} = {int(floor((len(self.__liste_elements) - 1) / self.__max_element_par_page()))}")
        return int(floor((len(self.__liste_elements) - 1) / self.__max_element_par_page()))

    def __limite_acceptable(self, index: int) -> bool:
        if index < 0:
            return False
        if index >= self.__max_element_par_page():
            return False
        return True

    def __changement_page_droite(self):
        if self.__page_courante < self.__nombre_de_page():
            logging.debug("Il y a une page suivante on y va")
            self.__page_courante += 1
            if self.__index_rapport_page(self.__index_ecran) >= len(self.__liste_elements):
                self.__index_ecran = len(self.__liste_elements) - (self.__max_element_par_page() * self.__nombre_de_page()) - 1
                logging.debug(f"La ligne selectionnée n'est pas accessible -> recalcul: {self.__index_ecran}")
            self.__affichage_element()

    def __changement_page_gauche(self):
        if self.__page_courante > 0:
            logging.debug("Il y a une page précédente on y va")
            self.__page_courante -= 1
            self.__affichage_element()

    def gere_touche(self, touche: Sequence) -> bool:
        if touche.egale(HAUT):
            logging.debug("Touche HAUT de la liste")
            nouvel_index = max(0, self.__index_ecran - 1)
            if nouvel_index != self.__index_ecran and len(self.__liste_elements) > 0:
                logging.debug("Deplacement de l'index vers le haut")
                if self.__limite_acceptable(nouvel_index):
                    self.__minitel.position(1, self.__position_par_index(nouvel_index))
                    self.__rendu_element(self.__liste_elements[self.__index_rapport_page(nouvel_index)], True, self.__index_rapport_page(nouvel_index))

                if self.__limite_acceptable(self.__index_ecran):
                    self.__minitel.position(1, self.__position_par_index(self.__index_ecran))
                    self.__rendu_element(self.__liste_elements[self.__index_rapport_page(self.__index_ecran)], False, self.__index_rapport_page(self.__index_ecran))

                self.__index_ecran = nouvel_index
            elif self.__page_courante > 0:
                self.__index_ecran = self.__max_element_par_page() - 1
                self.__changement_page_gauche()
            return True

        if touche.egale(BAS):
            logging.debug("Touche BAS de la liste")
            nouvel_index = min(self.__max_element_par_page() - 1, self.__index_ecran + 1)
            if nouvel_index != self.__index_ecran and self.__index_rapport_page(nouvel_index) < len(self.__liste_elements):
                logging.debug("Deplacement de l'index vers le bas")
                if self.__limite_acceptable(nouvel_index):
                    self.__minitel.position(1, self.__position_par_index(nouvel_index))
                    self.__rendu_element(self.__liste_elements[self.__index_rapport_page(nouvel_index)], True, self.__index_rapport_page(nouvel_index))

                if self.__limite_acceptable(self.__index_ecran):
                    self.__minitel.position(1, self.__position_par_index(self.__index_ecran))
                    self.__rendu_element(self.__liste_elements[self.__index_rapport_page(self.__index_ecran)], False, self.__index_rapport_page(self.__index_ecran))

                self.__index_ecran = nouvel_index

            elif self.__page_courante < self.__nombre_de_page():
                self.__index_ecran = 0
                self.__changement_page_droite()

            return True

        if touche.egale(DROITE):
            logging.debug(f"Touche DROITE de la liste {self.__page_courante} / {self.__nombre_de_page()}")
            self.__changement_page_droite()
            return True

        if touche.egale(GAUCHE):
            logging.debug(f"Touche GAUCHE de la liste {self.__page_courante} / {self.__nombre_de_page()}")
            self.__changement_page_gauche()
            return True

        if touche.egale(ENVOI):
            logging.debug("Touche ENVOI de la liste")
            if self.__callback_envoi is not None and self.__index_ecran >= 0:
                self.__callback_envoi(self.__liste_elements[self.__index_rapport_page(self.__index_ecran)])
                return False
            return True

        if touche.egale(ENTREE):
            logging.debug("Touche ENTREE de la liste")
            if self.__callback_entree is not None and self.__index_ecran >= 0:
                self.__callback_entree(self.__liste_elements[self.__index_rapport_page(self.__index_ecran)])
                return False
            return True

        return False
