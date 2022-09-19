__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from threading import Timer

import inject
from minitel.Minitel import Minitel
from minitel.constantes import HAUT, BAS
from minitel.ui.Conteneur import Conteneur
from minitel.ui.UI import UI
from pyobservable import Observable

from controleur.composant.AudioComposantControleur import AudioComposantControleur
from modele.composant.AudioModele import AudioModele
from service.minitel.MinitelConfiguration import CaracteresMinitel
from service.minitel.MinitelExtension import MinitelExtension


class AudioComposantVue(UI):
    __COLONNE_AFFICHAGE_COMPOSANT = 40
    __LIGNE_AFFICHAGE_COMPOSANT = 2
    __COULEUR = "jaune"
    __DELAI_EFFACEMENT_EN_SECONDES = 2

    __minitel_extension = inject.attr(MinitelExtension)
    __audio_composant_controleur = inject.attr(AudioComposantControleur)
    __audio_modele = inject.attr(AudioModele)
    __notificateur_evenement = inject.attr(Observable)
    __thread_effaceur: Timer

    def __init__(self, minitel: Minitel, conteneur: Conteneur):
        super().__init__(
            minitel=minitel,
            posx=AudioComposantVue.__COLONNE_AFFICHAGE_COMPOSANT,
            posy=AudioComposantVue.__LIGNE_AFFICHAGE_COMPOSANT,
            largeur=1,
            hauteur=20,
            couleur=AudioComposantVue.__COULEUR
        )
        self.__conteneur_hote = conteneur

    def affiche(self):
        logging.debug("Affichage du composant de volume : on affiche rien au démarrage")
        self.__notificateur_evenement.bind(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, self._dessin)

    def efface(self):
        self.__notificateur_evenement.unbind(AudioModele.EVENEMENT_CHANGEMENT_VOLUME, self._dessin)
        try:
            self.__thread_effaceur.cancel()
        except AttributeError:
            # l'effaceur n'a jamais été initialisé : cas du composant jamais affiché
            pass
        self.__efface()

    def gere_touche(self, sequence):

        if sequence.egale(HAUT):
            self.__audio_composant_controleur.action_augmenter_volume()
            return True

        if sequence.egale(BAS):
            self.__audio_composant_controleur.action_diminuer_volume()
            return True

        return False

    def _dessin(self, volume):
        logging.debug(f"Dessine le volume:{volume}")
        int_volume = int((AudioModele.MAX_VOLUME - volume) / 5)

        self.minitel.curseur(False)
        self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()

        self.__minitel_extension.position_couleur(self.posx, self.posy, self.couleur)
        if volume == AudioModele.MAX_VOLUME:
            self.minitel.envoyer(CaracteresMinitel.BARRE_HAUT_PLEIN.caractere)
        else:
            self.minitel.envoyer(CaracteresMinitel.BARRE_HAUT_VIDE.caractere)

        for i in range(1, 19):
            self.__minitel_extension.position_couleur(self.posx, self.posy + i, self.couleur)
            if i < int_volume:
                self.minitel.envoyer(CaracteresMinitel.BARRE_MILIEU_VIDE.caractere)
            else:
                self.minitel.envoyer(CaracteresMinitel.BARRE_MILIEU_PLEIN.caractere)

        self.__minitel_extension.position_couleur(self.posx, self.posy + 19, self.couleur)
        if volume == AudioModele.MIN_VOLUME:
            self.minitel.envoyer(CaracteresMinitel.BARRE_BAS_VIDE.caractere)
        else:
            self.minitel.envoyer(CaracteresMinitel.BARRE_BAS_PLEIN.caractere)

        self.__minitel_extension.revenir_jeu_caractere_standard()
        self.__replace_curseur()
        self.__demarrer_effacement_programme()

    def __replace_curseur(self):
        element = self.__conteneur_hote.element_actif
        if element is not None:
            self.minitel.position(element.posx + element.curseur_x - element.decalage, element.posy)
            self.minitel.curseur(True)

    def __demarrer_effacement_programme(self):
        try:
            if self.__thread_effaceur.is_alive():
                self.__thread_effaceur.cancel()
        except AttributeError:
            # l'effaceur n'a jamais été initialisé : cas du premier appel
            pass
        self.__thread_effaceur = Timer(AudioComposantVue.__DELAI_EFFACEMENT_EN_SECONDES, self.__efface)
        self.__thread_effaceur.start()

    def __efface(self):
        self.minitel.curseur(False)
        self.minitel.couleur("noir")
        for i in range(0, 20):
            self.minitel.position(self.posx, i + self.posy)
            self.minitel.envoyer(" ")
        self.__replace_curseur()
