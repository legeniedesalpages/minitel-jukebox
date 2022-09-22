__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from enum import Enum

import inject
import math
from minitel.Minitel import Minitel
from minitel.constantes import BAS, HAUT, SUITE, RETOUR
from minitel.ui.UI import UI
from pyobservable import Observable

from controleur.recherche.AbstractRechercheControleur import AbstractRechercheControleur
from modele.recherche.AbstractRechercheModele import AbstractRechercheModele, MouvementSelection, \
    EvenementRechercheModele
from service.minitel.MinitelExtension import MinitelExtension
from vue.bidule.Etiquette import Etiquette, Alignement


class EtatLigne(Enum):
    def __init__(self, couleur_cartouche, inversion_cartouche, couleur_ligne, inversion_ligne):
        self.couleur_cartouche = couleur_cartouche
        self.inversion_cartouche = inversion_cartouche
        self.couleur_ligne = couleur_ligne
        self.inversion_ligne = inversion_ligne

    INACTIF = "rouge", False, "rouge", False
    SELECTIONNE = "vert", True, "jaune", True
    NORMAL = "bleu", True, "jaune", False


class ResultatRechercheComposant(UI):
    __minitel_extension = inject.attr(MinitelExtension)
    __notificateur_evenement = inject.attr(Observable)

    def __init__(self, minitel: Minitel, posy, taille_cartouche,
                 recherche_modele: AbstractRechercheModele, recherche_controleur: AbstractRechercheControleur,
                 formateur_cartouche, formateur_ligne
                 ):
        super().__init__(
            minitel=minitel,
            posx=1,
            posy=posy,
            largeur=39,  # la dernière colonne est réservée
            hauteur=1 + 3 * 5 + 1,
            couleur=None
        )
        self.activable = True

        self.__recherche_modele = recherche_modele
        self.__recherche_controleur = recherche_controleur

        self.__formateur_cartouche = formateur_cartouche
        self.__formateur_ligne = formateur_ligne

        self._premier_affichage = True
        self._taille_cartouche = taille_cartouche
        self._taille_ligne = self.largeur - self._taille_cartouche - 1

        self.__notificateur_evenement.bind(EvenementRechercheModele.EVENEMENT_CHANGEMENT_RESULTAT, self._dessin)
        self.__notificateur_evenement.bind(EvenementRechercheModele.EVENEMENT_CHANGEMENT_SELECTION, self._dessin)
        self.__notificateur_evenement.bind(EvenementRechercheModele.EVENEMENT_ANNULATION_RECHERCHE, self._annulation)

    def fermer(self):
        self.__notificateur_evenement.unbind(EvenementRechercheModele.EVENEMENT_CHANGEMENT_RESULTAT, self._dessin)
        self.__notificateur_evenement.unbind(EvenementRechercheModele.EVENEMENT_CHANGEMENT_SELECTION, self._dessin)
        self.__notificateur_evenement.unbind(EvenementRechercheModele.EVENEMENT_ANNULATION_RECHERCHE, self._annulation)

    def _annulation(self):
        self._dessin(MouvementSelection.PAGE, est_actif=False)

    def _dessin(self, mouvement_selection: MouvementSelection = MouvementSelection.PAGE, est_actif=True):
        logging.debug(f"Dessin du composant des résultats de recherche: {mouvement_selection}")
        self.minitel.curseur(False)

        if mouvement_selection == MouvementSelection.MONTE:
            compteur = self.__recherche_modele.element_selectionne - 1
            if compteur % 5 == 4:
                self._dessin(MouvementSelection.PAGE)
            else:
                chanson = self.__recherche_modele.liste_resultat[compteur]
                self.__affichage_bloc_ligne(chanson, compteur % 5, True, est_actif)
                chanson = self.__recherche_modele.liste_resultat[compteur + 1]
                self.__affichage_bloc_ligne(chanson, compteur % 5 + 1, False, est_actif)

        elif mouvement_selection == MouvementSelection.DESCEND:
            compteur = self.__recherche_modele.element_selectionne - 1
            if compteur % 5 == 0:
                self._dessin(MouvementSelection.PAGE)
            else:
                chanson = self.__recherche_modele.liste_resultat[compteur]
                self.__affichage_bloc_ligne(chanson, compteur % 5, True, est_actif)
                chanson = self.__recherche_modele.liste_resultat[compteur - 1]
                self.__affichage_bloc_ligne(chanson, compteur % 5 - 1, False, est_actif)

        elif mouvement_selection == MouvementSelection.PAGE:
            self.minitel.position(1, self.posy)
            self.__affichage_separateur()

            page = math.floor((self.__recherche_modele.element_selectionne - 1) / 5)
            for compteur in range(0, 5):

                index = page * 5 + compteur
                if index < len(self.__recherche_modele.liste_resultat):
                    chanson = self.__recherche_modele.liste_resultat[index]
                    est_selectionne = (self.__recherche_modele.element_selectionne - 1) % 5 == compteur
                    self.__affichage_bloc_ligne(chanson, compteur, est_selectionne, est_actif)
                else:
                    self.__affichage_bloc_ligne(None, compteur, False, est_actif)

                self.minitel.effet(inversion=False)
                self.__affichage_separateur()

            self.__affichage_resume(page)
            self._premier_affichage = False

    def __affichage_resume(self, page):
        debut = page * 5 + 1
        fin = page * 5 + 5
        total = len(self.__recherche_modele.liste_resultat)
        texte = f"  résultats {debut} à {fin if fin < total else total} sur {total} "
        Etiquette.aligne(Alignement.DROITE, self.posy + 3 * 5 + 1, texte, "rouge").affiche()

    def __affichage_bloc_ligne(self, chanson, rang_element, selectionne, actif):

        texte_cartouche = self.__formateur_cartouche(chanson)

        texte_ligne = self.__formateur_ligne(chanson)

        etat_ligne = EtatLigne.INACTIF if not actif else EtatLigne.SELECTIONNE if selectionne else EtatLigne.NORMAL

        self.minitel.position(1, 1 + self.posy + rang_element * 3)
        self.__affichage_contenu_ligne(texte_cartouche, texte_ligne, etat_ligne)

    def __affichage_contenu_ligne(self, texte_cartouche: str, texte_ligne: str, etat_ligne: EtatLigne):

        taille_cartouche = self._taille_cartouche
        self.minitel.couleur(etat_ligne.couleur_cartouche)
        self.minitel.effet(inversion=etat_ligne.inversion_cartouche)
        sequence = texte_cartouche[:taille_cartouche].strip().rjust(taille_cartouche, " ")
        self.minitel.envoyer(sequence)

        taille_ligne = self._taille_ligne
        self.minitel.couleur(etat_ligne.couleur_ligne)
        self.minitel.effet(inversion=etat_ligne.inversion_ligne)
        sequence = " " + texte_ligne[:taille_ligne].strip().ljust(taille_ligne, " ")
        self.minitel.envoyer(sequence)
        self.minitel.effet(inversion=False)
        self.minitel.envoyer(" ")

        self.minitel.couleur(etat_ligne.couleur_cartouche)
        self.minitel.effet(inversion=etat_ligne.inversion_cartouche)
        sequence = texte_cartouche[taille_cartouche:taille_cartouche * 2].strip().rjust(taille_cartouche, " ")
        self.minitel.envoyer(sequence)

        self.minitel.couleur(etat_ligne.couleur_ligne)
        self.minitel.effet(inversion=etat_ligne.inversion_ligne)
        sequence = " " + texte_ligne[taille_ligne:taille_ligne * 2].strip().ljust(taille_ligne, " ")
        self.minitel.envoyer(sequence)
        self.minitel.effet(inversion=False)
        self.minitel.envoyer(" ")

    def __affichage_separateur(self):
        if self._premier_affichage:
            self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()
            self.minitel.couleur("rouge")
            self.minitel.repeter("-", 39)
            self.__minitel_extension.revenir_jeu_caractere_standard()

    def gere_touche(self, sequence):

        if sequence.egale(BAS):
            self.__recherche_controleur.resultat_recherche_suivant()
            return True

        if sequence.egale(HAUT):
            self.__recherche_controleur.resultat_recherche_precedent()
            return True

        if sequence.egale(SUITE):
            self.__recherche_controleur.resultat_recherche_page_suivante()
            return True

        if sequence.egale(RETOUR):
            self.__recherche_controleur.resultat_recherche_page_precedente()
            return True

        return False
