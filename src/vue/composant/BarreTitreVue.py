__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import logging
from threading import Timer
from typing import Optional

import inject
from minitel.Minitel import Minitel
from pyobservable import Observable

from modele.bluetooth.BluetoothModele import BluetoothModele
from modele.bluetooth.PeripheriqueBluetooth import PeripheriqueBluetooth
from modele.lecteur.JukeBoxModele import JukeBoxModele
from modele.wifi.Wifi import Wifi
from modele.wifi.WifiModele import WifiModele
from service.minitel.MinitelConstante import CaracteresMinitel
from service.minitel.MinitelExtension import MinitelExtension
from vue.bidule.Etiquette import Etiquette
from vue.bidule.Liste import Liste
from vue.bidule.Sablier import Sablier
from vue.bidule.Separateur import Separateur
from vue.commun.Affichable import Affichable


class BarreTitreVue(Affichable):
    __DELAI_EFFACEMENT_EN_SECONDES = 5

    __notificateur_evenement = inject.attr(Observable)
    __sablier = inject.attr(Sablier)
    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)

    def __init__(self, titre: str, bluetooth_modele: BluetoothModele, wifi_modele: WifiModele, callback_positionnement_curseur):
        self.__titre = titre
        self.__bluetooth_modele = bluetooth_modele
        self.__wifi_modele = wifi_modele
        self.__callback_positionnement_curseur = callback_positionnement_curseur
        self.__thread_effaceur = None

    def afficher(self):
        logging.debug("Affichage barre titre")
        self.__notificateur_evenement.bind(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE, self._mettre_a_jour_statut_blueooth)
        self.__notificateur_evenement.bind(WifiModele.EVENEMENT_WIFI_CHANGE, self._mettre_a_jour_statut_wifi)
        self.__notificateur_evenement.bind(Liste.EVENEMENT_LISTE_CHANGE_PAGE, self._mettre_a_jour_titre_page)
        self.__notificateur_evenement.bind(JukeBoxModele.EVENEMENT_NOTIFICATION, self._mettre_a_jour_notification)

        # Etiquette.centre(posy=0, texte="---oO Minitel JukeBox Oo---", couleur_texte=1)
        Etiquette.centre(posy=1, texte=self.__titre)
        Separateur.plein(posy=2)
        self._mettre_a_jour_statut_blueooth(self.__bluetooth_modele.peripherique_connecte)
        self._mettre_a_jour_statut_wifi(self.__wifi_modele.wifi)

    def _mettre_a_jour_notification(self, message: str):
        Separateur.plein(posy=2)
        Etiquette.centre(posy=2, texte=f"^{message}^"[:38], couleur_texte=5)
        self.__demarrer_effacement_programme()
        self.__callback_positionnement_curseur()

    def _efface(self):
        Separateur.plein(posy=2)
        self.__callback_positionnement_curseur()

    def _mettre_a_jour_titre_page(self, pagination: str):
        Etiquette.centre(posy=1, texte=f"{self.__titre}")
        Etiquette.droite(posy=1, texte=f"{pagination}", couleur_texte=2)
        self.__callback_positionnement_curseur()

    def _mettre_a_jour_statut_wifi(self, wifi: Optional[Wifi]):
        logging.info(f"Statut wifi doit être mis à jour: {wifi}")
        sablier_tournait_avant_maj = self.__sablier.arreter()

        self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()
        self.__minitel.position(colonne=3, ligne=1)
        if wifi is not None:
            self.__minitel.couleur(f"{wifi.force * 3 - 2}")
            logging.debug(f"Wifi force: {wifi.force}")
            self.__minitel.envoyer(CaracteresMinitel.WIFI_ON.caractere)
        else:
            self.__minitel.couleur("1")
            logging.debug("Pas de wifi")
            self.__minitel.envoyer(CaracteresMinitel.WIFI_OFF.caractere)
        self.__minitel_extension.revenir_jeu_caractere_standard()

        if sablier_tournait_avant_maj:
            self.__sablier.demarrer()

        self.__callback_positionnement_curseur()

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

        self.__callback_positionnement_curseur()

    def fermer(self):
        self.__notificateur_evenement.unbind(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE, self._mettre_a_jour_statut_blueooth)
        self.__notificateur_evenement.unbind(WifiModele.EVENEMENT_WIFI_CHANGE, self._mettre_a_jour_statut_wifi)
        self.__notificateur_evenement.unbind(Liste.EVENEMENT_LISTE_CHANGE_PAGE, self._mettre_a_jour_titre_page)
        self.__notificateur_evenement.unbind(JukeBoxModele.EVENEMENT_NOTIFICATION, self._mettre_a_jour_notification)
        if self.__thread_effaceur is not None and self.__thread_effaceur.is_alive():
            self.__thread_effaceur.cancel()

    def __demarrer_effacement_programme(self):
        if self.__thread_effaceur is not None and self.__thread_effaceur.is_alive():
            logging.debug("Un précédent effaceur était en cours, on l'annule")
            self.__thread_effaceur.cancel()

        logging.debug("Démarre le timer d'effacement")
        self.__thread_effaceur = Timer(BarreTitreVue.__DELAI_EFFACEMENT_EN_SECONDES, self._efface)
        self.__thread_effaceur.start()
