__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2023-11-20"
__version__ = "1.0.0"

import logging
import re
import subprocess
from typing import List, Optional

from modele.PeripheriqueBluetooth import PeripheriqueBluetooth


class BluetoothService:

    def __init__(self):
        self.__process_scan = None
        logging.debug("Initialisation service bluetooth")

    def initialiser(self):
        logging.info("Initialisation des services bluetooth")
        process_pairable = subprocess.Popen(["bluetoothctl", "pairable", "on"], stdout=subprocess.PIPE)
        process_pairable.kill()
        process_discoverable = subprocess.Popen(["bluetoothctl", "discoverbale", "on"], stdout=subprocess.PIPE)
        process_discoverable.kill()

    def scanner_peripheriques(self):
        logging.info("Lancement du scan des périphériques bluetooth")
        self.__process_scan = subprocess.Popen(["bluetoothctl", "scan", "on"], stdout=subprocess.PIPE)
        logging.debug("Scan des périphériques bluetooth en cours...")

    def arreter_scanner(self):
        logging.debug("Demande d'arrêt du scan des périphériques bluetooth")
        self.__process_scan.terminate()
        process_scan_off = subprocess.Popen(["bluetoothctl", "scan", "off"], stdout=subprocess.PIPE)
        process_scan_off.kill()
        logging.info("Arrêt du scan des périphériques bluetooth")

    @staticmethod
    def deconnecter_peripherique(adresse_mac):
        logging.debug(f"Deconnecter {adresse_mac}")
        BluetoothService.__operation(["bluetoothctl", "disconnect", adresse_mac], "Successful disconnected")

    @staticmethod
    def oublier_peripherique(adresse_mac):
        logging.debug(f"Oublier {adresse_mac}")
        BluetoothService.__operation(["bluetoothctl", "remove", adresse_mac], "Device has been removed")

    @staticmethod
    def associer_peripherique(adresse_mac):
        logging.debug(f"associer {adresse_mac}")
        BluetoothService.__operation(["bluetoothctl", "pair", adresse_mac], "Pairing successful")
        BluetoothService.__operation(["bluetoothctl", "trust", adresse_mac], "trust succeeded")
        BluetoothService.__operation(["bluetoothctl", "connect", adresse_mac], "Connection successful")
        logging.info(f"Association {adresse_mac} terminée")

    @staticmethod
    def peripherique_connecte() -> Optional[PeripheriqueBluetooth]:
        logging.debug("Recherche du peripherique connecté")
        process_paired_devices = subprocess.Popen(["bluetoothctl", "paired-devices"], stdout=subprocess.PIPE)
        paired_devices_lines = process_paired_devices.stdout.readlines()
        logging.debug(f"Nombre de peripherique appairés: {len(paired_devices_lines)}")
        process_paired_devices.kill()

        for line in paired_devices_lines:
            peripherique_parse = re.search(r"Device\s([A-Z0-9:]*)\s(.*)", line.decode('utf-8'))
            if peripherique_parse is not None:
                peripherique_parse_group = peripherique_parse.groups()
                peripherique_appaire = PeripheriqueBluetooth(
                    peripherique_parse_group[1],
                    peripherique_parse_group[0],
                    PeripheriqueBluetooth.TypeStatut.INCONNU)

                logging.debug(f"Peripherique connus: {peripherique_parse}")
                process_info = subprocess.Popen(["bluetoothctl", "info", peripherique_appaire.adresse_mac], stdout=subprocess.PIPE)
                lines_info = process_info.stdout.readlines()
                process_info.kill()
                if [i for i in lines_info if b"Connected: yes" in i]:
                    logging.debug(f" -> connecté !")
                    return peripherique_appaire
                else:
                    logging.debug(f" -> mais pas connecté")

        logging.debug("Aucun peripherique connecté trouvé")
        return None

    @staticmethod
    def lister_peripheriques() -> List[PeripheriqueBluetooth]:
        logging.debug("Début du listing des périphériques trouvés")
        process_devices = subprocess.Popen(["bluetoothctl", "devices"], stdout=subprocess.PIPE)
        liste_peripherique_trouve = []
        lines = process_devices.stdout.readlines()
        process_devices.kill()
        logging.info(f"Nombre de périphériques bluetooth trouvées : {len(lines)}")
        for peripherique_brut in lines:
            peripherique_parse = re.search(r"Device\s([A-Z0-9:]*)\s(.*)", peripherique_brut.decode('utf-8'))
            if peripherique_parse is not None:
                peripherique_parse_group = peripherique_parse.groups()
                peripherique = PeripheriqueBluetooth(peripherique_parse_group[1], peripherique_parse_group[0], PeripheriqueBluetooth.TypeStatut.INCONNU)
                liste_peripherique_trouve.append(peripherique)

        logging.debug("Fin du listing des périphériques trouvés")
        return liste_peripherique_trouve

    @staticmethod
    def __operation(action: List[str], chaine_resultat_attendu: str) -> bool:
        logging.debug(f"Execute {action}")
        process = subprocess.Popen(action, stdout=subprocess.PIPE)
        lignes_resultat = process.stdout.readlines()
        if [i for i in lignes_resultat if str.encode(chaine_resultat_attendu) in i]:
            logging.debug(f"Résultat {chaine_resultat_attendu} trouvé!")
            return True
        logging.debug(f"Résultat attendu '{chaine_resultat_attendu}' non trouvé dans : {lignes_resultat}")
        process.kill()
        return False
