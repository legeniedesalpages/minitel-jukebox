__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2023-11-20"
__version__ = "1.0.0"

import logging
from typing import List, Optional, Tuple

from modele.PeripheriqueBluetooth import PeripheriqueBluetooth


class BluetoothModele:
    liste_peripherique: List[PeripheriqueBluetooth]
    peripherique_selectionne: Optional[PeripheriqueBluetooth]
    peripherique_connecte: Optional[PeripheriqueBluetooth]

    def __init__(self):
        self.liste_peripherique = []
        self.peripherique_selectionne = None

    def doit_rafraichir_liste(self, nouvelle_liste: List[PeripheriqueBluetooth],
                              nouveau_peripherique_connecte: Optional[PeripheriqueBluetooth]) -> Tuple[bool, bool, int]:

        est_nouveau_peripherique_connecte = False
        adresse_mac_nouveau_peripherique_connecte = self.__retourne_adresse_mac(nouveau_peripherique_connecte)
        adresse_mac_peripherique_connecte = self.__retourne_adresse_mac(self.peripherique_connecte)
        if adresse_mac_nouveau_peripherique_connecte != adresse_mac_peripherique_connecte:
            self.peripherique_connecte = nouveau_peripherique_connecte
            est_nouveau_peripherique_connecte = True

        if self.peripherique_connecte is not None:
            nouvelle_liste[:] = (value for value in nouvelle_liste if
                                 value.adresse_mac != self.peripherique_connecte.adresse_mac)
        nouvelle_liste.sort(key=lambda p: p.nom)

        if not self.__est_liste_identique(nouvelle_liste):
            difference_taille = len(self.liste_peripherique) - len(nouvelle_liste)
            logging.info(f"Rafraichissement de la liste des périphériques {difference_taille}")

            self.liste_peripherique = nouvelle_liste

            # deselectionne le peripherique selectionne si le peripherique dispartait des peripherique disponible
            if self.peripherique_selectionne is not None and not any(
                    x.adresse_mac == self.peripherique_selectionne.adresse_mac for x in self.liste_peripherique):
                self.peripherique_selectionne = None

            return True, est_nouveau_peripherique_connecte, difference_taille if difference_taille > 0 else 0

        return False, est_nouveau_peripherique_connecte, 0

    def navigation_liste(self, descend: bool) -> bool:
        index = -1
        change = False
        if self.peripherique_selectionne is not None:
            for i in range(len(self.liste_peripherique)):
                if self.liste_peripherique[i].adresse_mac == self.peripherique_selectionne.adresse_mac:
                    index = i

        if descend:
            if self.peripherique_selectionne is None:
                self.peripherique_selectionne = self.liste_peripherique[0]
                change = True
            else:
                if index != len(self.liste_peripherique) - 1:
                    self.peripherique_selectionne = self.liste_peripherique[index + 1]
                    change = True

        else:
            if self.peripherique_selectionne is None:
                self.peripherique_selectionne = self.liste_peripherique[-1]
                change = True
            else:
                if index != 0:
                    self.peripherique_selectionne = self.liste_peripherique[index - 1]
                    change = True

        return change

    def __est_liste_identique(self, nouvelle_liste: List[PeripheriqueBluetooth]) -> bool:

        if len(self.liste_peripherique) != len(nouvelle_liste):
            logging.debug("Taille des listes différentes, il y a eu changement")
            return False

        for i in range(len(self.liste_peripherique)):
            if nouvelle_liste[i].adresse_mac != self.liste_peripherique[i].adresse_mac:
                logging.debug(
                    f"Listes différentes : {nouvelle_liste[i].adresse_mac} != {self.liste_peripherique[i].adresse_mac}")
                return False

        return True

    @staticmethod
    def __retourne_adresse_mac(peripherique: Optional[PeripheriqueBluetooth]):
        if peripherique is None:
            return ""
        else:
            return peripherique.adresse_mac
