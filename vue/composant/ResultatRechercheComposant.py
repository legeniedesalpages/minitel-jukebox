__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
from minitel.Minitel import Minitel
from minitel.ui.Conteneur import Conteneur
from minitel.ui.UI import UI
from pyobservable import Observable

from modele.recherche.AbstractRechercheModele import AbstractRechercheModele, MouvementSelection
from service.minitel.MinitelExtension import MinitelExtension
from vue.bidule.Etiquette import Etiquette, Alignement


class ResultatRechercheComposant(UI):
    __LIGNE_AFFICHAGE_COMPOSANT = 4
    __COULEUR = "blanc"

    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)
    __notificateur_evenement = inject.attr(Observable)

    def __init__(self, conteneur: Conteneur, recherche_modele: AbstractRechercheModele):
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

    def affiche(self):
        logging.debug("Affichage du composant de resultat de recherche: on affiche rien au démarrage")
        self._dessin(MouvementSelection.PAGE)
        self.__notificateur_evenement.bind(AbstractRechercheModele.EVENEMENT_CHANGEMENT_SELECTION, self._dessin)

    def efface(self):
        self.__notificateur_evenement.unbind(AbstractRechercheModele.EVENEMENT_CHANGEMENT_SELECTION, self._dessin)

    def _dessin(self, mouvement_selection: MouvementSelection):
        logging.debug(f"Dessin du composant dse résultat de recherche: {mouvement_selection}")
        self.__minitel.curseur(False)

        if mouvement_selection == MouvementSelection.PAGE:
            Etiquette.aligne(Alignement.DROITE, 4, "Nombre résultats: 20").affiche()
            self.__minitel.position(1, 5)
            self.__minitel.couleur("rouge")
            self.__minitel.repeter("-", 40)

            compteur = 0
            for chanson in self.__recherche_modele.liste_resultat:
                compteur += 1
                inversion = compteur == self.__recherche_modele.element_selectionne
                self.__affichage_element(chanson, compteur, inversion)

        elif mouvement_selection == MouvementSelection.MONTE:
            compteur = self.__recherche_modele.element_selectionne
            self.__affichage_element(self.__recherche_modele.liste_resultat[compteur - 1], compteur, True)
            self.__affichage_element(self.__recherche_modele.liste_resultat[compteur], compteur + 1, False)

        elif mouvement_selection == MouvementSelection.DESCEND:
            compteur = self.__recherche_modele.element_selectionne
            self.__affichage_element(self.__recherche_modele.liste_resultat[compteur - 1], compteur, True)
            self.__affichage_element(self.__recherche_modele.liste_resultat[compteur - 2], compteur - 1, False)

    def __affichage_element(self, chanson, compteur, inversion):
        if chanson.duree.count(":") == 0:
            duree = chanson.duree.rjust(5, " ")[:5]
        elif chanson.duree.count(":") == 1:
            duree = chanson.duree.rjust(5, "0")[:5]
        else:
            duree = " >1h "
        self.__minitel.position(1, 3 + compteur * 3)
        if inversion:
            self.__minitel.couleur("vert")
        else:
            self.__minitel.couleur("bleu")
        self.__minitel.effet(inversion=True)
        self.__minitel.envoyer(duree)
        self.__minitel.couleur("jaune")
        self.__minitel.effet(inversion=inversion)
        self.__minitel.envoyer(" " + chanson.titre[:33].ljust(34, " "))

        self.__minitel.position(1, 4 + compteur * 3)
        if inversion:
            self.__minitel.couleur("vert")
        else:
            self.__minitel.couleur("bleu")
        self.__minitel.effet(inversion=True)
        self.__minitel.envoyer(" ".rjust(5, " "))
        self.__minitel.couleur("jaune")
        self.__minitel.effet(inversion=inversion)
        self.__minitel.envoyer(" " + chanson.titre[33:66].ljust(34, " "))

        self.__minitel.position(1, 5 + compteur * 3)
        self.__minitel.couleur("rouge")
        self.__minitel.repeter("-", 40)
