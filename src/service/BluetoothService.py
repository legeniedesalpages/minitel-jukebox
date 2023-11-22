import logging
import re
import subprocess
from typing import List, Optional

from modele.PeripheriqueBluetooth import PeripheriqueBluetooth


class BluetoothService:

    def __init__(self):
        self.__process_scan = None
        logging.info("Initialisation service bluetooth")

    def scanner_peripheriques(self):
        logging.info("Lancement du scan des périphériques bluetooth")
        self.__process_scan = subprocess.Popen(["bluetoothctl", "scan", "on"], stdout=subprocess.PIPE)
        logging.debug("Scan des périphériques bluetooth en cours...")

    def arreter_scanner(self):
        logging.debug("Demande d'arrêt du scan des périphériques bluetooth")
        self.__process_scan.terminate()
        subprocess.Popen(["bluetoothctl", "scan", "off"], stdout=subprocess.PIPE)
        logging.info("Arrêt du scan des périphériques bluetooth")

    @staticmethod
    def deconnecte_peripherique(adresse_mac):
        logging.debug(f"Deconnecter {adresse_mac}")
        BluetoothService.__operation(["bluetoothctl", "disconnect", adresse_mac], "Successful disconnected")
        BluetoothService.__operation(["bluetoothctl", "remove", adresse_mac], "Device has been removed")

    @staticmethod
    def associer(adresse_mac):
        logging.debug(f"associer {adresse_mac}")
        BluetoothService.__operation(["bluetoothctl", "pair", adresse_mac], "Pairing successful")
        BluetoothService.__operation(["bluetoothctl", "trust", adresse_mac], "trust succeeded")
        BluetoothService.__operation(["bluetoothctl", "connect", adresse_mac], "Connection successful")
        logging.info(f"Association {adresse_mac} terminée")

    @staticmethod
    def peripherique_connecte() -> Optional[PeripheriqueBluetooth]:
        logging.debug("Recherche du peripherique connecté")
        proc_liste_appaire = subprocess.Popen(["bluetoothctl", "paired-devices"], stdout=subprocess.PIPE)
        lines = proc_liste_appaire.stdout.readlines()
        logging.debug(f"Nombre de peripherique appairés: {len(lines)}")

        for line in lines:
            peripherique_parse = re.search(r"Device\s([A-Z0-9:]*)\s(.*)", line.decode('utf-8')).groups()
            peripherique_appaire = PeripheriqueBluetooth(
                peripherique_parse[1],
                peripherique_parse[0],
                PeripheriqueBluetooth.TypeStatut.INCONNU)

            logging.debug(f"Peripherique connus: {peripherique_parse}")
            proc_info = subprocess.Popen(["bluetoothctl", "info", peripherique_appaire.adresse_mac],
                                         stdout=subprocess.PIPE)
            lines_info = proc_info.stdout.readlines()
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
        proc = subprocess.Popen(["bluetoothctl", "devices"], stdout=subprocess.PIPE)
        liste_peripherique_trouve = []
        lines = proc.stdout.readlines()
        logging.info(f"Nombre de périphériques trouvées : {len(lines)}")
        for peripherique_brut in lines:
            peripherique_parse = re.search(r"Device\s([A-Z0-9:]*)\s(.*)", peripherique_brut.decode('utf-8')).groups()
            peripherique = PeripheriqueBluetooth(
                peripherique_parse[1],
                peripherique_parse[0],
                PeripheriqueBluetooth.TypeStatut.INCONNU)

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
        logging.debug(f"Résultat {chaine_resultat_attendu} non trouvé dans : {lignes_resultat}")
        return False
