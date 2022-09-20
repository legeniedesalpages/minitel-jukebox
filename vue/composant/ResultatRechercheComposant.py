__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
import math
from minitel.Minitel import Minitel
from minitel.constantes import BAS, HAUT
from minitel.ui.Conteneur import Conteneur
from minitel.ui.UI import UI
from pyobservable import Observable

from controleur.recherche.AbstractRechercheControleur import AbstractRechercheControleur
from modele.recherche.AbstractRechercheModele import AbstractRechercheModele, MouvementSelection, \
    EvenementRechercheModele
from service.minitel.MinitelExtension import MinitelExtension


class ResultatRechercheComposant(UI):
    __LIGNE_AFFICHAGE_COMPOSANT = 4
    __COULEUR = "blanc"

    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)
    __notificateur_evenement = inject.attr(Observable)

    def __init__(self, conteneur: Conteneur, recherche_modele: AbstractRechercheModele, recherche_controleur: AbstractRechercheControleur):
        super().__init__(
            minitel=self.__minitel,
            posx=1,
            posy=ResultatRechercheComposant.__LIGNE_AFFICHAGE_COMPOSANT,
            largeur=1,
            hauteur=20,
            couleur=ResultatRechercheComposant.__COULEUR
        )
        self.__conteneur_hote = conteneur
        self.__recherche_modele = recherche_modele
        self.__recherche_controleur = recherche_controleur
        self.__affiche = False

    def affiche(self):
        logging.debug("Affichage du composant de resultat de recherche: on affiche rien au démarrage")
        self._dessin(MouvementSelection.PAGE)
        self.__affiche = True
        self.__notificateur_evenement.bind(EvenementRechercheModele.EVENEMENT_CHANGEMENT_SELECTION, self._dessin)

    def efface(self):
        logging.debug("Efface la précédente recherche")
        if self.__affiche:
            self.__notificateur_evenement.unbind(EvenementRechercheModele.EVENEMENT_CHANGEMENT_SELECTION, self._dessin)
            self.__minitel.position(1, ResultatRechercheComposant.__LIGNE_AFFICHAGE_COMPOSANT)
            self.__minitel.efface("finecran")
            self.__affiche = False

    def _dessin(self, mouvement_selection: MouvementSelection):
        logging.debug(
            f"Dessin du composant dse résultat de recherche: {mouvement_selection}, {self.__recherche_modele.element_selectionne}")
        self.__minitel.curseur(False)

        if mouvement_selection == MouvementSelection.MONTE:
            compteur = self.__recherche_modele.element_selectionne - 1
            if compteur % 5 == 4:
                self._dessin(MouvementSelection.PAGE)
            else:
                self.__affichage_element(self.__recherche_modele.liste_resultat[compteur], compteur % 5 + 1, True)
                self.__affichage_element(self.__recherche_modele.liste_resultat[compteur + 1], compteur % 5 + 2, False)

        elif mouvement_selection == MouvementSelection.DESCEND:
            compteur = self.__recherche_modele.element_selectionne - 1
            if compteur % 5 == 0:
                self._dessin(MouvementSelection.PAGE)
            else:
                self.__affichage_element(self.__recherche_modele.liste_resultat[compteur], compteur % 5 + 1, True)
                self.__affichage_element(self.__recherche_modele.liste_resultat[compteur - 1], compteur % 5, False)

        elif mouvement_selection == MouvementSelection.PAGE:
            self.__minitel.position(1, 5)
            self.__minitel.couleur("rouge")
            self.__minitel.repeter("-", 40)

            for compteur in range(0, 5):
                page = math.floor((self.__recherche_modele.element_selectionne - 1) / 5)
                index = page * 5 + compteur
                if index < len(self.__recherche_modele.liste_resultat):
                    chanson = self.__recherche_modele.liste_resultat[index]
                    inversion = (self.__recherche_modele.element_selectionne - 1) % 5 == compteur
                    self.__affichage_element(chanson, compteur + 1, inversion)
                else:
                    self.__affichage_element(None, compteur + 1, False)

    def __affichage_element(self, chanson, compteur, inversion):
        if chanson is not None and chanson.duree is not None:
            if chanson.duree.count(":") == 0:
                duree = chanson.duree.rjust(5, " ")[:5]
            elif chanson.duree.count(":") == 1:
                duree = chanson.duree.rjust(5, "0")[:5]
            else:
                duree = " >1h "
        else:
            duree = "     "

        self.__minitel.position(1, 3 + compteur * 3)
        if inversion:
            self.__minitel.couleur("vert")
        else:
            self.__minitel.couleur("bleu")
        self.__minitel.effet(inversion=True)
        self.__minitel.envoyer(duree)
        self.__minitel.couleur("jaune")
        self.__minitel.effet(inversion=inversion)
        if chanson is not None:
            self.__minitel.envoyer(" " + chanson.titre[:33].ljust(34, " "))
        else:
            self.__minitel.repeter(" ", 39)

        self.__minitel.position(1, 4 + compteur * 3)
        if inversion:
            self.__minitel.couleur("vert")
        else:
            self.__minitel.couleur("bleu")
        self.__minitel.effet(inversion=True)
        self.__minitel.envoyer(" ".rjust(5, " "))
        self.__minitel.couleur("jaune")
        self.__minitel.effet(inversion=inversion)
        if chanson is not None:
            self.__minitel.envoyer(" " + chanson.titre[33:66].ljust(34, " "))
        else:
            self.__minitel.repeter(" ", 39)

        self.__minitel.position(1, 5 + compteur * 3)
        self.__minitel.couleur("rouge")
        self.__minitel.repeter("-", 40)

    def gere_touche(self, sequence):

        if sequence.egale(BAS):
            self.__recherche_controleur.resultat_recherche_suivant()
            return True

        if sequence.egale(HAUT):
            self.__recherche_controleur.resultat_recherche_precedent()
            return True
