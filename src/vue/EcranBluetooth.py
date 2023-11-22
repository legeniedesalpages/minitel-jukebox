__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2023-11-20"
__version__ = "1.0.0"

import logging
from queue import Empty

import inject
from minitel.Minitel import Minitel
from minitel.Sequence import Sequence
from minitel.constantes import SOMMAIRE, BAS, HAUT, ENVOI, ENTREE, ANNULATION
from minitel.ui.Conteneur import Conteneur

from controleur.BluetoothControleur import BluetoothControleur
from modele.BluetoothModele import BluetoothModele
from service.minitel.MinitelExtension import MinitelExtension
from vue.EcranInterface import EcranInterface
from vue.bidule.Etiquette import Etiquette, Alignement
from vue.bidule.Sablier import Sablier


class EcranBluetoothVue(EcranInterface):
    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)
    __sablier = inject.attr(Sablier)

    def __init__(self, bluetooth_controleur: BluetoothControleur, bluetooth_modele: BluetoothModele):
        self.__bluetooth_controleur = bluetooth_controleur
        self.__bluetooth_modele = bluetooth_modele
        self._conteneur = Conteneur(self.__minitel, 1, 1, 40, 24)

    def afficher(self):
        titre = "Périphériques ^Bluetooth^"
        self._conteneur.ajoute(Etiquette.aligne(Alignement.CENTRE, 1, titre, "blanc"))
        self.__minitel_extension.separateur(2, "rouge")

        self._conteneur.ajoute(Etiquette.aligne(Alignement.GAUCHE, 3, "Connecté", "blanc"))
        self.__minitel.position(1, 4)
        self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()
        self.__minitel.couleur("rouge")
        self.__minitel.repeter("-", 39)
        self.__minitel_extension.revenir_jeu_caractere_standard()
        self.__afficher_peripherique_connecte()

        self._conteneur.ajoute(Etiquette.aligne(Alignement.GAUCHE, 7, "Périphériques détectés", "blanc"))
        self.__minitel.position(1, 8)
        self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()
        self.__minitel.couleur("rouge")
        self.__minitel.repeter("-", 39)
        self.__minitel_extension.revenir_jeu_caractere_standard()

        self._conteneur.ajoute(Etiquette.aligne(Alignement.DROITE, 24, "Déconnecter prériphérique ^ANNULATION^"))

        self._conteneur.affiche()
        self.__sablier.demarrer()

        sequence = self.__recupere_sequence()
        while not sequence.egale(SOMMAIRE):

            if sequence.longueur == 0:
                doit_rafraichir_liste, doit_rafraichir_peripherique_connecte, effacement_ligne_en_trop = self.__bluetooth_controleur.rafraichir_liste()
                if doit_rafraichir_liste:
                    self.__afficher_liste(effacement_ligne_en_trop)
                if doit_rafraichir_peripherique_connecte:
                    self.__afficher_peripherique_connecte()

            else:
                change = False
                if sequence.egale(BAS):
                    change = self.__bluetooth_controleur.descend()
                elif sequence.egale(HAUT):
                    change = self.__bluetooth_controleur.monte()
                elif sequence.egale(ENVOI) or sequence.egale(ENTREE):
                    self.__bluetooth_controleur.associer_peripherique_selectionne()
                elif sequence.egale(ANNULATION):
                    change = self.__bluetooth_controleur.deconnecte()

                if change:
                    self.__afficher_liste(0)

            sequence = self.__recupere_sequence()

        self.__sablier.arreter()
        self.__minitel.efface('vraimenttout')

    def __afficher_peripherique_connecte(self):
        logging.info(f"Peripherique connecte a afficher : {self.__bluetooth_modele.peripherique_connecte}")
        self.__minitel.position(1, 5)
        self.__minitel.couleur("vert")
        if self.__bluetooth_modele.peripherique_connecte is None:
            sequence = " - Aucun périphérique connecté".ljust(40, " ")
            self.__minitel.envoyer(sequence)
        else:
            nom = f" - {self.__bluetooth_modele.peripherique_connecte.nom[:39]}"
            sequence = nom.rstrip().ljust(40, " ")
            self.__minitel.envoyer(sequence)

    def __afficher_liste(self, nombre_ligne_a_effacer):
        self.__sablier.arreter()
        self.__minitel.position(1, 9)
        for peripherique in self.__bluetooth_modele.liste_peripherique:
            nom = f" - {peripherique.nom[:39]}"
            sequence = nom.rstrip().ljust(40, " ")

            if self.__bluetooth_modele.peripherique_selectionne is not None \
                    and self.__bluetooth_modele.peripherique_selectionne.adresse_mac == peripherique.adresse_mac:
                self.__minitel.effet(inversion=True)
                self.__minitel.envoyer(sequence)
                self.__minitel.effet(inversion=False)
            else:
                self.__minitel.envoyer(sequence)

        for i in range(nombre_ligne_a_effacer):
            self.__minitel.envoyer("".ljust(40, " "))

        self.__sablier.demarrer()

    def __recupere_sequence(self) -> Sequence:
        try:
            return self.__minitel.recevoir_sequence(bloque=True, attente=2)
        except Empty:
            return Sequence()
