__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
from minitel.Minitel import Minitel
from minitel.ui.UI import UI
from pyobservable import Observable

from modele.LecteurModele import LecteurModele


class LecteurWidget(UI):
    __TOUCHE_RETOUR = [19, 66]
    __TOUCHE_SUITE = [19, 72]
    __TOUCHE_REPETITION = [19, 67]
    __TOUCHE_ANNULATION = [19, 69]

    __LIGNE = 24

    @inject.autoparams()
    def __init__(self, minitel: Minitel, lecteur_modele: LecteurModele, notificateur_evenement: Observable):
        super().__init__(minitel, 1, 1, 1, 1, "noir")
        self.__minitel = minitel
        self.__lecteur_modele = lecteur_modele
        notificateur_evenement.bind(LecteurModele.EVENEMENT_RECHERCHE_CHANSON, self.recherche_chanson)
        notificateur_evenement.bind(LecteurModele.EVENEMENT_CHANGEMENT_CHANSON, self.changement_chanson)
        notificateur_evenement.bind(LecteurModele.EVENEMENT_PAUSE, self.pause_chanson)
        notificateur_evenement.bind(LecteurModele.EVENEMENT_REPRISE, self.reprise_chanson)

    def affiche(self):
        self.__dessine("Lecteur arrété")

    def recherche_chanson(self, texte):
        self.__dessine(f"Recherche {texte}")

    def changement_chanson(self, texte):
        self.__dessine(f"Lecture: {texte}")

    def pause_chanson(self, texte):
        self.__dessine(f"Pause")

    def reprise_chanson(self, texte):
        self.__dessine(f"Lecture: {texte}")

    def __dessine(self, texte):
        self.__minitel.position(1, LecteurWidget.__LIGNE)
        self.__minitel.couleur("blanc")
        self.__minitel.effet(inversion=True)
        self.__minitel.envoyer(texte.ljust(40, " ")[:40])

    def gere_touche(self, sequence):
        touche = sequence.valeurs
        logging.debug(f"Touche appuyée: {touche}")

        if touche == LecteurWidget.__TOUCHE_REPETITION:
            self.__lecteur_modele.jouer_chanson("eye tiger")
            return True

        if touche == LecteurWidget.__TOUCHE_ANNULATION:
            self.__lecteur_modele.pause_ou_reprendre()
            return True
