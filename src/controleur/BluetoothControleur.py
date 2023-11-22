__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2023-11-20"
__version__ = "1.0.0"

from typing import Tuple

import inject

from modele.BluetoothModele import BluetoothModele
from modele.JukeBoxModele import EvenementSortieEcran
from service.BluetoothService import BluetoothService
from vue.EcranInterface import EcranInterface


class BluetoothControleur:
    __ecran: EcranInterface
    __bluetoothService = inject.attr(BluetoothService)

    def __init__(self, bluetooth_modele: BluetoothModele):
        self.__bluetooth_modele = bluetooth_modele

    def enregistrer_vue(self, ecran: EcranInterface):
        self.__ecran = ecran

    def afficher_ecran_configuration(self) -> EvenementSortieEcran:
        self.__bluetooth_modele.peripherique_connecte = self.__bluetoothService.peripherique_connecte()
        self.__bluetoothService.scanner_peripheriques()
        self.__ecran.afficher()
        self.__bluetoothService.arreter_scanner()
        return EvenementSortieEcran.AFFICHER_RECHERCHE

    def descend(self) -> bool:
        return self.__bluetooth_modele.navigation_liste(descend=True)

    def monte(self) -> bool:
        return self.__bluetooth_modele.navigation_liste(descend=False)

    def rafraichir_liste(self) -> Tuple[bool, bool, int]:
        nouveau_peripherique_connecte = self.__bluetoothService.peripherique_connecte()
        nouvelle_liste = self.__bluetoothService.lister_peripheriques()
        return self.__bluetooth_modele.doit_rafraichir_liste(nouvelle_liste, nouveau_peripherique_connecte)

    def associer_peripherique_selectionne(self):
        if self.__bluetooth_modele.peripherique_selectionne is not None:
            self.__bluetoothService.associer(self.__bluetooth_modele.peripherique_selectionne.adresse_mac)

    def deconnecte(self):
        if self.__bluetooth_modele.peripherique_connecte is not None:
            self.__bluetoothService.deconnecte_peripherique(self.__bluetooth_modele.peripherique_connecte.adresse_mac)
