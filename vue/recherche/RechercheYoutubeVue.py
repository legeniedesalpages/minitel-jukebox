__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
from minitel.constantes import ENTREE, ANNULATION
from minitel.ui.ChampTexte import ChampTexte
from minitel.ui.Label import Label
from pyobservable import Observable

from controleur.recherche.RechercheYoutubeControleur import RechercheYoutubeControleur
from modele.recherche.AbstractRechercheModele import AbstractRechercheModele, EvenementRechercheModele
from vue.bidule.Etiquette import Etiquette, Alignement
from vue.composant.ResultatRechercheComposant import ResultatRechercheComposant
from vue.recherche.AbstractRechercheVue import AbstractRechercheVue


class RechercheYoutubeVue(AbstractRechercheVue):
    __notificateur_evenement = inject.attr(Observable)
    __resultat_recherche: ResultatRechercheComposant

    def __init__(self, recherche_controleur: RechercheYoutubeControleur, recherche_modele: AbstractRechercheModele):
        super().__init__(recherche_controleur, recherche_modele)

        titre = "Recherche dans les services ^Youtube^"
        self._conteneur.ajoute(Etiquette.aligne(Alignement.CENTRE, 1, titre, "blanc"))
        self._minitel_extension.separateur(2, "rouge")
        self._conteneur.ajoute(Label(self._minitel, 1, 3, "Chanson:", "vert"))
        self.__champ_saisie = ChampTexte(self._minitel, 10, 3, 29, 60)
        self._conteneur.ajoute(self.__champ_saisie)
        self._conteneur.ajoute(Etiquette.aligne(Alignement.DROITE, 23, "Lancer la recherche ^ENTREE^"))
        self._conteneur.ajoute(Etiquette.aligne(Alignement.DROITE, 24, "Lancer la chanson ^ENVOI^"))
        self._conteneur.element_actif = self.__champ_saisie

    def afficher(self):
        self.__notificateur_evenement.bind(EvenementRechercheModele.EVENEMENT_CHANGEMENT_RESULTAT,
                                           self._afficher_liste_resultat)
        self.__notificateur_evenement.bind(EvenementRechercheModele.EVENEMENT_ANNULATION_RECHERCHE,
                                           self._annulation_recherche)
        super(RechercheYoutubeVue, self).afficher()

    def fermer(self):
        super(RechercheYoutubeVue, self).fermer()
        self.__notificateur_evenement.unbind(EvenementRechercheModele.EVENEMENT_CHANGEMENT_RESULTAT,
                                             self._afficher_liste_resultat)
        self.__notificateur_evenement.unbind(EvenementRechercheModele.EVENEMENT_ANNULATION_RECHERCHE,
                                             self._annulation_recherche)

    def _afficher_liste_resultat(self):
        logging.debug("Affiche la liste des resultat")
        self.__efface_resultat_recherche()
        self.__resultat_recherche = ResultatRechercheComposant(self._conteneur, self._recherche_modele, self._recherche_controleur)
        self._conteneur.ajoute(self.__resultat_recherche)
        self._conteneur.element_actif = self.__resultat_recherche
        self.__resultat_recherche.affiche()

    def _annulation_recherche(self):
        logging.info("Efface le texte de la recherche")
        self.__champ_saisie.valeur = ""
        self.__champ_saisie.curseur_x = 0
        self.__champ_saisie.decalage = 0
        self.__champ_saisie.affiche()
        logging.info("Efface le composant de résultat")
        self.__efface_resultat_recherche()
        self._conteneur.element_actif = self.__champ_saisie
        self.__champ_saisie.gere_arrivee()

    def __efface_resultat_recherche(self):
        try:
            if self.__resultat_recherche is not None:
                self.__resultat_recherche.efface()
                self._conteneur.elements.remove(self.__resultat_recherche)
                self.__resultat_recherche = None
        except AttributeError:
            pass

    def _gerer_touche(self, sequence):

        if sequence.egale(ENTREE):
            if len(self.__champ_saisie.valeur.strip()) > 0:
                self._recherche_controleur.lancer_recherche(self.__champ_saisie.valeur)
            return True

        if sequence.egale(ANNULATION):
            self._recherche_controleur.annuler_recherche()
            return True
