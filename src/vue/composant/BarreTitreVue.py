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
from vue.bidule.Etiquette import Etiquette
from vue.bidule.Sablier import Sablier
from vue.bidule.Separateur import Separateur


class BarreTitreVue(Affichable):
    __notificateur_evenement = inject.attr(Observable)
    __sablier = inject.attr(Sablier)
    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)

    def __init__(self, titre: str, bluetooth_modele: BluetoothModele):
        self.__titre = titre
        self.__bluetooth_modele = bluetooth_modele

    def afficher(self):
        logging.debug("Affichage barre titre")
        self.__notificateur_evenement.bind(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE, self._mettre_a_jour_statut_blueooth)
        Etiquette.centre(posy=1, texte=self.__titre)
        Separateur.plein(posy=2)
        self._mettre_a_jour_statut_blueooth(self.__bluetooth_modele.peripherique_connecte)

    def _mettre_a_jour_statut_blueooth(self, peripehrique: Optional[PeripheriqueBluetooth]):
        logging.info(f"Statut bluetooth doit être mis à jour: {peripehrique}")
        sablier_tournait_avant_maj = self.__sablier.arreter()

        self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()
        if peripehrique is not None:
            self.__minitel_extension.position_couleur(posy=1, posx=1, couleur="blanc")
            self.__minitel.envoyer(CaracteresMinitel.BLUETOOTH_ON.caractere)
        else:
            self.__minitel_extension.position_couleur(posy=1, posx=1, couleur="rouge")
            self.__minitel.envoyer(CaracteresMinitel.BLUETOOTH_OFF.caractere)
        self.__minitel_extension.revenir_jeu_caractere_standard()

        if sablier_tournait_avant_maj:
            self.__sablier.demarrer()

    def fermer(self):
        self.__notificateur_evenement.unbind(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE, self._mettre_a_jour_statut_blueooth)
