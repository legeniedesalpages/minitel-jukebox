__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-31"
__version__ = "1.0.0"

import logging
import re
import subprocess
from typing import AnyStr, List, Optional

from modele.wifi.Wifi import Wifi


class WifiService:

    def __init__(self):
        pass

    def recuperer_wifi(self) -> Optional[Wifi]:
        process = subprocess.Popen(["iwconfig"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lignes_brut: List[AnyStr] = process.stdout.readlines()
        process.kill()

        if (lignes_brut is None) or (len(lignes_brut) == 0):
            logging.info("Pas d'info wifi remontée par iwconfig")
            return None

        chaine_brut: str = ''.join(map(str, lignes_brut))

        parse = re.search(r".*ESSID:\"(.*)\".*Link Quality=([0-9]*)/([0-9]*)", chaine_brut)
        if parse is None:
            logging.info("Pas d'info wifi trouvée dans le retour iwconfig")
            return None

        group = parse.groups()
        if group is None or len(group) != 3:
            logging.info("Toutes les infos wifi non pas été trouvées dans le retour iwconfig")
            return None

        force = int(int(group[1]) / int(group[2]) * Wifi.FORCE_MAX)
        return Wifi(group[0], force)
