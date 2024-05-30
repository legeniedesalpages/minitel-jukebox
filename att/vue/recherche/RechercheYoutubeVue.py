__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
import re

import inject
from minitel.Minitel import Minitel
from minitel.constantes import ENTREE, ANNULATION, ENVOI
from minitel.ui.ChampTexte import ChampTexte
from minitel.ui.Label import Label
from pyobservable import Observable

from controleur.recherche.RechercheYoutubeControleur import RechercheYoutubeControleur
from modele.recherche.AbstractRechercheModele import AbstractRechercheModele, EvenementRechercheModele
from vue.bidule.Etiquette import Etiquette, Alignement
from vue.bidule.Sablier import Sablier
from vue.composant.ResultatRechercheComposant import ResultatRechercheComposant
from vue.recherche.AbstractRechercheVue import AbstractRechercheVue


class RechercheYoutubeVue(AbstractRechercheVue):
    REGEX_NETTOYAGE_TITRE = r'[^A-Za-z0-9\'éèêâîôûùçàëïöü*$!:;,?./&(-_)=+@# ]+'

    __notificateur_evenement = inject.attr(Observable)
    __sablier = inject.attr(Sablier)
    __minitel = inject.attr(Minitel)

    def __init__(self, recherche_controleur: RechercheYoutubeControleur, recherche_modele: AbstractRechercheModele):
        super().__init__(recherche_controleur, recherche_modele)

        titre = "Recherche dans les services ^Youtube^"
        self._conteneur.ajoute(Etiquette.aligne(Alignement.CENTRE, 1, titre, "blanc"))
        self._minitel_extension.separateur(2, "rouge")
        self._conteneur.ajoute(Label(self._minitel, 1, 3, "Chanson:", "vert"))
        self.__champ_saisie = ChampTexte(self._minitel, 10, 3, 29, 60, "eye in the sky")
        self._conteneur.ajoute(self.__champ_saisie)
        self.__resultat_recherche = ResultatRechercheComposant(self.__minitel, 5, 5, recherche_modele,
                                                               recherche_controleur, self._formater_recherche_cartouche,
                                                               self._formater_recherche_ligne)
        self._conteneur.ajoute(self.__resultat_recherche)
        self.__etiquette_touche_entree = Etiquette.aligne(Alignement.DROITE, 23, "Lancer la recherche ^ENTREE^")
        self._conteneur.ajoute(self.__etiquette_touche_entree)
        self._conteneur.ajoute(Etiquette.aligne(Alignement.DROITE, 24, "Lancer la chanson ^ENVOI^"))
        self._conteneur.element_actif = self.__champ_saisie

    def afficher(self):
        self.__notificateur_evenement.bind(EvenementRechercheModele.EVENEMENT_ANNULATION_RECHERCHE,
                                           self._annulation_recherche)
        self.__notificateur_evenement.bind(EvenementRechercheModele.EVENEMENT_CHANGEMENT_RESULTAT,
                                           self._afficher_resultat_recherche)
        super(RechercheYoutubeVue, self).lancer()

    def fermer(self):
        super(RechercheYoutubeVue, self).fermer()
        self.__resultat_recherche.fermer()
        self.__notificateur_evenement.unbind(EvenementRechercheModele.EVENEMENT_ANNULATION_RECHERCHE,
                                             self._annulation_recherche)
        self.__notificateur_evenement.unbind(EvenementRechercheModele.EVENEMENT_CHANGEMENT_RESULTAT,
                                             self._afficher_resultat_recherche)

    @staticmethod
    def _formater_recherche_cartouche(chanson):
        if chanson is not None and chanson.duree is not None:
            if chanson.duree.count(":") == 0:
                return chanson.duree.rjust(5, " ")[:5]
            elif chanson.duree.count(":") == 1:
                return chanson.duree.rjust(5, "0")[:5]
            else:
                return " >1h "
        else:
            return ""

    def _formater_recherche_ligne(self, chanson):
        return "" if not chanson else re.sub(self.REGEX_NETTOYAGE_TITRE, '', chanson.titre)

    def _annulation_recherche(self, conserver_texte_saisie):
        if not conserver_texte_saisie:
            logging.info("Efface le texte de la recherche")
            self.__champ_saisie.valeur = ""
            self.__champ_saisie.curseur_x = 0
            self.__champ_saisie.decalage = 0

        self.__remplacer_etiquette(Etiquette.aligne(Alignement.DROITE, 23, "          Lancer la recherche ^ENTREE^"))
        self._conteneur.element_actif = self.__champ_saisie
        self.__champ_saisie.affiche()

    def _afficher_resultat_recherche(self):
        self._conteneur.element_actif = self.__resultat_recherche
        self.__remplacer_etiquette(Etiquette.aligne(Alignement.DROITE, 23, "Ajouter à la liste de lecture ^ENTREE^"))

    def __remplacer_etiquette(self, nouvelle_etiquette):
        self._conteneur.elements.remove(self.__etiquette_touche_entree)
        self.__etiquette_touche_entree = nouvelle_etiquette
        self._conteneur.ajoute(self.__etiquette_touche_entree)
        self.__etiquette_touche_entree.affiche()

    def gerer_touche(self, sequence):

        if sequence.egale(ENVOI):
            logging.info("Recherche et lit la chanson sans passer par l'affichage du résultat de la recherche")
            if len(self.__champ_saisie.valeur.strip()) > 0:
                self._recherche_controleur.chercher_et_lire(self.__champ_saisie.valeur)
            return True

        if sequence.egale(ENTREE):
            if len(self.__champ_saisie.valeur.strip()) > 0:
                self.__sablier.demarrer()
                self._recherche_controleur.lancer_recherche(self.__champ_saisie.valeur)
            return True

        if sequence.egale(ANNULATION):
            if self._conteneur.element_actif is self.__champ_saisie:
                self.__champ_saisie.valeur = ""
                self.__champ_saisie.curseur_x = 0
                self.__champ_saisie.decalage = 0
                self.__champ_saisie.affiche()
                return True

        return False
