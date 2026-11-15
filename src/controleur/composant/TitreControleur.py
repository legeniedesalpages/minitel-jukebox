__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import logging
import threading

from modele.bluetooth.BluetoothModele import BluetoothModele
from modele.wifi.WifiModele import WifiModele
from service.bluetooth.BluetoothService import BluetoothService
from service.wifi.WifiService import WifiService
from service.ErreurService import ErreurService


class TitreControleur:
    __evenement_attente: threading.Event

    def __init__(self, __bluetooth_modele: BluetoothModele, __bluetooth_service: BluetoothService,
                 __wifi_modele: WifiModele, __wifi_service: WifiService):
        logging.debug("Démarrage du titre controleur")
        self.__bluetooth_modele = __bluetooth_modele
        self.__bluetooth_service = __bluetooth_service
        self.__wifi_modele = __wifi_modele
        self.__wifi_service = __wifi_service
        self.__fin_raffraichissement = False
        threading.Thread(target=self._raffraichissement).start()

    def _raffraichissement(self):
        self.__evenement_attente = threading.Event()
        while not self.__fin_raffraichissement:
            # todo : fixer le timeout
            if not self.__evenement_attente.wait(timeout=1000):
                try:
                    peripherique = self.__bluetooth_service.peripherique_connecte()
                    self.__bluetooth_modele.verification_changement_peripherique_apaire(peripherique)
                    wifi = self.__wifi_service.recuperer_wifi()
                    self.__wifi_modele.verification_changement_wifi(wifi)
                except Exception as erreur:
                    ErreurService.signaler("Actualisation de l'etat Bluetooth et Wi-Fi", erreur)

    def arreter(self):
        logging.info("Arret du raffraichissement de l'état bluetooth et wifi")
        self.__fin_raffraichissement = True
        if self.__evenement_attente is not None:
            self.__evenement_attente.set()
