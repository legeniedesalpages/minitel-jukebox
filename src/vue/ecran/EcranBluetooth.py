__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2023-11-20"
__version__ = "1.0.0"

import logging
from typing import Optional

from minitel.Sequence import Sequence

from controleur.bluetooth.BluetoothControleur import BluetoothControleur
from modele.bluetooth.BluetoothModele import BluetoothModele
from modele.bluetooth.PeripheriqueBluetooth import PeripheriqueBluetooth
from vue.commun.AbstractEcran import AbstractEcran
from vue.bidule.Etiquette import Etiquette
from vue.bidule.Separateur import Separateur


class EcranBluetooth(AbstractEcran):
    __bluetooth_controleur: BluetoothControleur
    __bluetooth_modele: BluetoothModele

    def __init__(self, bluetooth_controleur: BluetoothControleur, modeles: dict[str, object]):
        super().__init__(bluetooth_controleur, modeles)
        logging.debug("Bluetooth vue init")
        # noinspection PyTypeChecker
        self.__bluetooth_modele = modeles["bluetooth"]
        self.__bluetooth_controleur = bluetooth_controleur

    def _get_titre_ecran(self) -> str:
        return "Périphériques ^BLUETOOTH^"

    def _affichage_initial(self):
        self._notificateur_evenement.bind(BluetoothModele.EVENEMENT_LISTE_PERIPHERIQUE_BLUETOOTH_CHANGE, self._afficher_liste_peripherique)
        self._notificateur_evenement.bind(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE, self._afficher_peripherique_connecte)
        self._notificateur_evenement.bind(BluetoothModele.EVENEMENT_SELECTION_DANS_LISTE_PERIPHERIQUE_CHANGE, self._changer_selection)

        Etiquette.gauche(posy=3, texte="Connecté")
        Separateur.leger(posy=4)

        Etiquette.gauche(7, "Périphériques détectés", "blanc")
        Separateur.leger(posy=8)

        Etiquette.droite(22, "Continuer ^SUITE^")
        Etiquette.droite(23, "Déconnecter prériphérique ^ANNULATION^")

        # lance une première fois l'affichage pour ne pas avoir à attendre la première mise à jour
        self._afficher_peripherique_connecte(self.__bluetooth_modele.peripherique_connecte)

    def fermer(self):
        self._notificateur_evenement.unbind(BluetoothModele.EVENEMENT_LISTE_PERIPHERIQUE_BLUETOOTH_CHANGE, self._afficher_liste_peripherique)
        self._notificateur_evenement.unbind(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE, self._afficher_peripherique_connecte)
        self._notificateur_evenement.unbind(BluetoothModele.EVENEMENT_SELECTION_DANS_LISTE_PERIPHERIQUE_CHANGE, self._changer_selection)
        self._sablier.arreter()

    def _afficher_peripherique_connecte(self, peripehrique: Optional[PeripheriqueBluetooth]):
        self._sablier.arreter()
        logging.info(f"Périphérique connecté à afficher : {self.__bluetooth_modele.peripherique_connecte}")

        if self.__bluetooth_modele.peripherique_connecte is None:
            texte = " - Aucun périphérique connecté"
        else:
            texte = f" - {self.__bluetooth_modele.peripherique_connecte.nom}"
        self._minitel_extension.envoyer_ligne(posy=5, texte=texte, couleur="vert")

        self._sablier.demarrer()

    def _changer_selection(self):
        logging.debug("Affichage du changement de la sélection dans la liste des périphériques")
        self._afficher_liste_peripherique(0)

    def _afficher_liste_peripherique(self, nombre_ligne_a_effacer):
        self._sablier.arreter()
        posy = 8
        for peripherique in self.__bluetooth_modele.liste_peripherique:
            posy += 1
            if self.__bluetooth_modele.peripherique_selectionne is not None and self.__bluetooth_modele.peripherique_selectionne.adresse_mac == peripherique.adresse_mac:
                self._minitel_extension.envoyer_ligne(posy=posy, texte=f" > {peripherique.nom[:39]}", inversion=True)
            else:
                self._minitel_extension.envoyer_ligne(posy=posy, texte=f" - {peripherique.nom[:39]}")

        for i in range(nombre_ligne_a_effacer):
            self._minitel_extension.effacer_ligne(posy + i + 1)

        self._sablier.demarrer()

    def _get_callback_curseur(self):
        pass

    def _gere_touche(self, touche: Sequence) -> bool:
        return False
