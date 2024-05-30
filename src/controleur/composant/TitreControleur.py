__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import logging
import threading
import time

from modele.BluetoothModele import BluetoothModele
from service.BluetoothService import BluetoothService


class TitreControleur:

    def __init__(self, __bluetooth_modele: BluetoothModele, __bluetooth_service: BluetoothService):
        logging.debug("Démarrage du titre controleur")
        self.__bluetooth_modele = __bluetooth_modele
        self.__bluetooth_service = __bluetooth_service
        self.__fin_raffraichissement_bluetooth = False
        thread_raffraichissement_bluetooth = threading.Thread(target=self._raffraichissement_bluetooth)
        thread_raffraichissement_bluetooth.start()

    def _raffraichissement_bluetooth(self):
        while not self.__fin_raffraichissement_bluetooth:
            time.sleep(10)
            peripherique = self.__bluetooth_service.peripherique_connecte()
            logging.debug(f"Recherche une mise à jour état bluetooth {peripherique}")
            self.__bluetooth_modele.verification_changement_peripherique_apaire(peripherique)

    def arreter(self):
        logging.info("Arret du raffraichissement de l'état bluetooth")
        self.__fin_raffraichissement_bluetooth = True
