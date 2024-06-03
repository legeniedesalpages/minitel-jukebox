__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2023-11-20"
__version__ = "1.0.0"

import logging
import threading
import time
from typing import Optional

import inject
from minitel.Sequence import Sequence
from minitel.constantes import BAS, HAUT, ENVOI, ENTREE, ANNULATION, SOMMAIRE, SUITE

from controleur.AbstractControleur import AbstractControleur
from controleur.PeutGererTouche import PeutGererTouche
from modele.BluetoothModele import BluetoothModele
from service.BluetoothService import BluetoothService


class BluetoothControleur(AbstractControleur):
    __bluetooth_service: BluetoothService = inject.attr(BluetoothService)

    __bluetooth_modele: BluetoothModele

    def __init__(self, controleurs_pouvant_gerer_touche: dict[str, PeutGererTouche], modeles: dict[str, object]):
        super().__init__(controleurs_pouvant_gerer_touche, modeles)
        logging.debug("bluetooth controleur init")
        # noinspection PyTypeChecker
        self.__bluetooth_modele = modeles["bluetooth"]

        #    ****************************
        # self.__liste_lecture: ListeLectureModele = modeles["liste_lecture"]
        # # self.__liste_lecture.ajouter_chanson(Chanson(identifiant_video="", titre="test", duree=0, url_image=""))
        # # self.__liste_lecture.ajouter_chanson(Chanson(identifiant_video="", titre="test a la limite du bord mais vraiment.", duree=0, url_image=""))
        # # self.__liste_lecture.ajouter_chanson(Chanson(identifiant_video="", titre="test sdf sdf sd fs df sdf s df sd f sf s df s df sd f sdf s df s df sd f sdf s df", duree=0, url_image=""))
        # self.__liste_lecture.chanson_suivante()
        # self.__liste_lecture.progression_chanson_courante = None
        # self.__liste_lecture.est_en_pause = False
        #    ****************************

        self.__fin_rafraichissement_liste_peripherique = False

    def lancer(self):

        self.__bluetooth_modele.peripherique_connecte = self.__bluetooth_service.peripherique_connecte()
        if self.__bluetooth_modele.peripherique_connecte is not None:
            logging.info(f"Peripherique connecte: {self.__bluetooth_modele.peripherique_connecte}, on ne passe pas par l'ecran bluetooth")
            return
        else:
            logging.info("Affichage de l'ecran bluetooth car il n'y a pas de peripherique connecte")

        # gère la mise à jour en tâche de fond de la liste des périphériques bluetooth
        declencheur = threading.Thread(target=self._rafraichir_liste)
        declencheur.start()

        self.__bluetooth_service.initialiser()
        self.__bluetooth_service.scanner_peripheriques()

        self._vue.afficher()

        logging.debug("Descativation du raffraichissement de la liste des périphériques")
        self.__fin_rafraichissement_liste_peripherique = True
        logging.debug("Fin de l'affichage ecran bluetooth")
        self.__bluetooth_service.arreter_scanner()

    def _gere_touche(self, touche: Sequence) -> Optional[bool]:
        if touche.egale(SUITE):
            logging.debug("Fin de la configuration Bluetooth")
            return True
        if touche.egale(SOMMAIRE):
            logging.debug("Sommaire ecran bluetooth: on ne sort pas")
            return False
        if touche.egale(BAS):
            logging.debug("Descendre dans la liste des peripheriques")
            self.__descend()
            return False
        elif touche.egale(HAUT):
            logging.debug("Monte dans la liste des peripheriques")
            self.__monte()
            return False
        elif touche.egale(ENVOI) or touche.egale(ENTREE):
            self.__associer_peripherique_selectionne()
            return False
        elif touche.egale(ANNULATION):
            self.__deconnecte()
            return False
        return None

    def __descend(self):
        self.__bluetooth_modele.navigation_liste(descend=True)

    def __monte(self):
        self.__bluetooth_modele.navigation_liste(descend=False)

    def __associer_peripherique_selectionne(self):
        if self.__bluetooth_modele.peripherique_selectionne is not None:
            self.__bluetooth_service.associer_peripherique(self.__bluetooth_modele.peripherique_selectionne.adresse_mac)

    def __deconnecte(self):
        if self.__bluetooth_modele.peripherique_connecte is not None:
            self.__bluetooth_service.deconnecter_peripherique(self.__bluetooth_modele.peripherique_connecte.adresse_mac)
            self.__bluetooth_service.oublier_peripherique(self.__bluetooth_modele.peripherique_connecte.adresse_mac)

    def _rafraichir_liste(self):
        while not self.__fin_rafraichissement_liste_peripherique:
            logging.debug("Rafraichissement de la liste des peripheriques")
            nouveau_peripherique_connecte = self.__bluetooth_service.peripherique_connecte()
            nouvelle_liste = self.__bluetooth_service.lister_peripheriques()
            self.__bluetooth_modele.doit_rafraichir_liste(nouvelle_liste, nouveau_peripherique_connecte)
            time.sleep(2)
