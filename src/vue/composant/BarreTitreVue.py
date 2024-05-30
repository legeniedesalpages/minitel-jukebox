__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import logging
from typing import Optional

import inject
from minitel.Minitel import Minitel
from pyobservable import Observable

from modele.BluetoothModele import BluetoothModele
from modele.PeripheriqueBluetooth import PeripheriqueBluetooth
from service.minitel.MinitelConstante import CaracteresMinitel
from service.minitel.MinitelExtension import MinitelExtension
from vue.Affichable import Affichable
from vue.bidule.Etiquette import Etiquette, Alignement
from vue.bidule.Sablier import Sablier


class BarreTitreVue(Affichable):
    __notificateur_evenement = inject.attr(Observable)
    __sablier = inject.attr(Sablier)

    def __init__(self, minitel: Minitel, titre: str, bluetooth_modele: BluetoothModele):
        self.__minitel = minitel
        self.__titre = titre
        self.__notificateur_evenement.bind(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE, self._mettre_a_jour_statut_blueooth)
        self.__bluetooth_modele = bluetooth_modele

    def afficher(self):
        logging.debug("Affichage barre titre")
        Etiquette.aligne(Alignement.CENTRE, 1, self.__titre, "blanc").affiche()
        MinitelExtension.separateur(self.__minitel, 2, "rouge")
        self._mettre_a_jour_statut_blueooth(self.__bluetooth_modele.peripherique_connecte)

    def _mettre_a_jour_statut_blueooth(self, peripehrique: Optional[PeripheriqueBluetooth]):
        logging.info("Statut bluetooth doit être mis à jour")
        sablier_tournait_avant_maj = self.__sablier.arreter()
        logging.debug(f"Le sablier tournait il avant la maj ? : {sablier_tournait_avant_maj}")

        MinitelExtension.demarrer_affichage_jeu_caractere_redefinit(self.__minitel)
        if peripehrique is not None:
            MinitelExtension.position_couleur(self.__minitel, 1, 1, "blanc")
            self.__minitel.envoyer(CaracteresMinitel.BLUETOOTH.caractere)
        else:
            MinitelExtension.position_couleur(self.__minitel, 1, 1, "rouge")
            self.__minitel.envoyer(CaracteresMinitel.BLUETOOTH_OFF.caractere)
        MinitelExtension.revenir_jeu_caractere_standard(self.__minitel)

        if sablier_tournait_avant_maj:
            self.__sablier.demarrer()

    def fermer(self):
        self.__notificateur_evenement.unbind(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE, self._mettre_a_jour_statut_blueooth)
