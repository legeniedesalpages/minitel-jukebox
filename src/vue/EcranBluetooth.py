__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2023-11-20"
__version__ = "1.0.0"

import logging
from typing import Optional

import inject
from minitel.Minitel import Minitel
from minitel.ui.Conteneur import Conteneur
from pyobservable import Observable

from controleur.BluetoothControleur import BluetoothControleur
from modele.BluetoothModele import BluetoothModele
from modele.PeripheriqueBluetooth import PeripheriqueBluetooth
from service.minitel.MinitelExtension import MinitelExtension
from vue.AbstractEcran import AbstractEcran
from vue.bidule.Etiquette import Etiquette, Alignement
from vue.bidule.Sablier import Sablier


class EcranBluetooth(AbstractEcran):
    __sablier = inject.attr(Sablier)
    __notificateur_evenement = inject.attr(Observable)

    __bluetooth_controleur: BluetoothControleur
    __bluetooth_modele: BluetoothModele

    def __init__(self, minitel: Minitel, bluetooth_controleur: BluetoothControleur, modeles: dict[str, object]):
        super().__init__(minitel, bluetooth_controleur, modeles)
        logging.info("Bluetooth vue init")
        self.__bluetooth_controleur = bluetooth_controleur
        # noinspection PyTypeChecker
        self.__bluetooth_modele = modeles["bluetooth"]

    def _get_titre_ecran(self) -> str:
        return "Périphériques ^BLUETOOTH^"

    def _affichage_initial(self):
        self.__notificateur_evenement.bind(BluetoothModele.EVENEMENT_LISTE_PERIPHERIQUE_BLUETOOTH_CHANGE, self._afficher_liste_peripherique)
        self.__notificateur_evenement.bind(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE, self._afficher_peripherique_connecte)
        self.__notificateur_evenement.bind(BluetoothModele.EVENEMENT_SELECTION_DANS_LISTE_PERIPHERIQUE_CHANGE, self._changer_selection)

        self.__conteneur = Conteneur(self._minitel, 1, 1, 40, 24)
        self.__conteneur.ajoute(Etiquette.aligne(Alignement.GAUCHE, 3, "Connecté", "blanc"))
        self._minitel.position(1, 4)
        MinitelExtension.demarrer_affichage_jeu_caractere_redefinit(self._minitel)
        self._minitel.couleur("rouge")
        self._minitel.repeter("-", 39)
        MinitelExtension.revenir_jeu_caractere_standard(self._minitel)

        self.__conteneur.ajoute(Etiquette.aligne(Alignement.GAUCHE, 7, "Périphériques détectés", "blanc"))
        self._minitel.position(1, 8)
        MinitelExtension.demarrer_affichage_jeu_caractere_redefinit(self._minitel)
        self._minitel.couleur("rouge")
        self._minitel.repeter("-", 39)
        MinitelExtension.revenir_jeu_caractere_standard(self._minitel)

        self.__conteneur.ajoute(Etiquette.aligne(Alignement.DROITE, 22, "Continuer ^SUITE^"))
        self.__conteneur.ajoute(Etiquette.aligne(Alignement.DROITE, 23, "Déconnecter prériphérique ^ANNULATION^"))

        self.__conteneur.affiche()
        self._afficher_peripherique_connecte(None)

    def fermer(self):
        self.__notificateur_evenement.unbind(BluetoothModele.EVENEMENT_LISTE_PERIPHERIQUE_BLUETOOTH_CHANGE, self._afficher_liste_peripherique)
        self.__notificateur_evenement.unbind(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE, self._afficher_peripherique_connecte)
        self.__notificateur_evenement.unbind(BluetoothModele.EVENEMENT_SELECTION_DANS_LISTE_PERIPHERIQUE_CHANGE, self._changer_selection)
        self.__sablier.arreter()

    def _afficher_peripherique_connecte(self, peripehrique: Optional[PeripheriqueBluetooth]):
        self.__sablier.arreter()
        logging.info(f"Peripherique connecte a afficher : {self.__bluetooth_modele.peripherique_connecte}")
        self._minitel.position(1, 5)
        self._minitel.couleur("vert")
        if self.__bluetooth_modele.peripherique_connecte is None:
            sequence = " - Aucun périphérique connecté".ljust(40, " ")
            self._minitel.envoyer(sequence)
        else:
            nom = f" - {self.__bluetooth_modele.peripherique_connecte.nom[:39]}"
            sequence = nom.rstrip().ljust(40, " ")
            self._minitel.envoyer(sequence)
        self.__sablier.demarrer()

    def _changer_selection(self):
        self._afficher_liste_peripherique(0)

    def _afficher_liste_peripherique(self, nombre_ligne_a_effacer):
        self.__sablier.arreter()
        self._minitel.position(1, 9)
        for peripherique in self.__bluetooth_modele.liste_peripherique:
            nom = f" - {peripherique.nom[:39]}"
            sequence = nom.rstrip().ljust(40, " ")

            if self.__bluetooth_modele.peripherique_selectionne is not None and self.__bluetooth_modele.peripherique_selectionne.adresse_mac == peripherique.adresse_mac:
                self._minitel.effet(inversion=True)
                self._minitel.envoyer(sequence)
                self._minitel.effet(inversion=False)
            else:
                self._minitel.envoyer(sequence)

        for i in range(nombre_ligne_a_effacer):
            self._minitel.envoyer("".ljust(40, " "))

        self.__sablier.demarrer()
