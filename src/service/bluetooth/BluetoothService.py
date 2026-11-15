__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2023-11-20"
__version__ = "1.0.0"

import logging
import re
import subprocess
from typing import List, Optional

from modele.bluetooth.PeripheriqueBluetooth import PeripheriqueBluetooth
from service.ErreurService import ErreurService


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
        if self.__process_scan is not None:
            self.__process_scan.terminate()
            self.__process_scan.wait(timeout=3)
            self.__process_scan = None
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
    def associer_peripherique(adresse_mac) -> bool:
        logging.info(f"Demarrage de l'association Bluetooth avec {adresse_mac}")
        informations = BluetoothService.__informations_peripherique(adresse_mac)

        if informations is None or "Connected: yes" not in informations:
            if informations is None or "Paired: yes" not in informations:
                if not BluetoothService.__operation(
                        ["bluetoothctl", "pair", adresse_mac], "Pairing successful"):
                    logging.error(f"Echec de l'appairage Bluetooth avec {adresse_mac}")
                    return False

            if informations is None or "Trusted: yes" not in informations:
                if not BluetoothService.__operation(
                        ["bluetoothctl", "trust", adresse_mac], "trust succeeded"):
                    logging.error(f"Echec de l'autorisation Bluetooth avec {adresse_mac}")
                    return False

            if not BluetoothService.__operation(
                    ["bluetoothctl", "connect", adresse_mac], "Connection successful"):
                logging.error(
                    f"Connexion Bluetooth impossible avec {adresse_mac}. "
                    "Verifiez que le peripherique est allume, en mode Bluetooth et a portee.")
                return False

        logging.info(f"Connexion Bluetooth reussie avec {adresse_mac}")
        return True

    @staticmethod
    def __informations_peripherique(adresse_mac) -> Optional[str]:
        try:
            process = subprocess.run(
                ["bluetoothctl", "info", adresse_mac],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=10,
                check=False
            )
        except (OSError, subprocess.TimeoutExpired):
            logging.exception(f"Impossible de lire l'etat Bluetooth de {adresse_mac}")
            return None

        if process.returncode != 0:
            logging.error(
                f"Lecture de l'etat Bluetooth de {adresse_mac} echouee "
                f"(code {process.returncode}): {process.stdout.strip()}")
            return None
        return process.stdout

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
                process_info = subprocess.Popen(["bluetoothctl", "info", peripherique_appaire.adresse_mac],
                                                stdout=subprocess.PIPE)
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
                peripherique = PeripheriqueBluetooth(peripherique_parse_group[1], peripherique_parse_group[0],
                                                     PeripheriqueBluetooth.TypeStatut.INCONNU)
                liste_peripherique_trouve.append(peripherique)

        logging.debug("Fin du listing des périphériques trouvés")
        return liste_peripherique_trouve

    @staticmethod
    def __operation(action: List[str], chaine_resultat_attendu: str) -> bool:
        logging.info(f"Execution de la commande Bluetooth: {' '.join(action)}")
        try:
            process = subprocess.run(
                action,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=30,
                check=False
            )
        except subprocess.TimeoutExpired:
            ErreurService.signaler(
                f"Commande Bluetooth {' '.join(action[1:])}",
                RuntimeError("Le peripherique ne repond pas (delai de 30 secondes depasse)."))
            return False
        except OSError as erreur:
            ErreurService.signaler(f"Commande Bluetooth {' '.join(action[1:])}", erreur)
            return False

        sortie = process.stdout.strip()
        if process.returncode == 0 and chaine_resultat_attendu in sortie:
            logging.info(f"Commande Bluetooth reussie: {' '.join(action)}")
            return True
        logging.error(
            f"Echec de la commande Bluetooth {' '.join(action)} "
            f"(code {process.returncode}); resultat attendu '{chaine_resultat_attendu}', "
            f"sortie: {sortie or '(aucune sortie)'}")
        lignes_erreur = [ligne for ligne in sortie.splitlines() if "Failed" in ligne or "Error" in ligne]
        detail = " ".join(lignes_erreur) or f"Resultat attendu absent: {chaine_resultat_attendu}"
        ErreurService.signaler(f"Commande Bluetooth {' '.join(action[1:])}", RuntimeError(detail))
        return False
