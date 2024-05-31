__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-31"
__version__ = "1.0.0"

import logging
from typing import Optional

import inject
from pyobservable import Observable

from modele.wifi.Wifi import Wifi


class WifiModele:
    EVENEMENT_WIFI_CHANGE = "EvenementWifiChange"

    __notificateur_evenement = inject.attr(Observable)

    wifi: Optional[Wifi]

    def __init__(self):
        self.wifi = None

    def verification_changement_wifi(self, nouveau_wifi: Optional[Wifi]):
        if self.wifi is None and nouveau_wifi is None:
            logging.debug("Aucun changement de wifi: pas de wifi")

        elif self.wifi is None and nouveau_wifi is not None:
            logging.debug(f"Connexion au wifi: {nouveau_wifi}")
            self.wifi = nouveau_wifi
            self.__notificateur_evenement.notify(self.EVENEMENT_WIFI_CHANGE, nouveau_wifi)

        elif self.wifi is not None and nouveau_wifi is None:
            logging.debug("Perte du wifi")
            self.wifi = None
            self.__notificateur_evenement.notify(self.EVENEMENT_WIFI_CHANGE, None)

        elif self.wifi is not None and (self.wifi.force != nouveau_wifi.force or self.wifi.nom != nouveau_wifi.nom):
            logging.debug(f"Changement de statut wifi: {nouveau_wifi}")
            self.wifi = nouveau_wifi
            self.__notificateur_evenement.notify(self.EVENEMENT_WIFI_CHANGE, nouveau_wifi)

        else:
            logging.debug("Aucun changement de wifi")
