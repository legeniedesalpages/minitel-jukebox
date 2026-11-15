__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
import textwrap
from typing import Optional

import inject
from minitel.Sequence import Sequence
from minitel.constantes import SOMMAIRE

from configuration.MVCCreateur import MVCCreateur
from controleur.bluetooth.BluetoothControleur import BluetoothControleur
from controleur.commun.AbstractControleur import AbstractControleur
from controleur.commun.PeutGererTouche import PeutGererTouche
from controleur.composant.AudioControleur import AudioControleur
from controleur.composant.LecteurControleur import LecteurControleur
from controleur.composant.TitreControleur import TitreControleur
from controleur.recherche.BibliothequeSpotifyControleur import BibliothequeSpotifyControleur
from controleur.recherche.YoutubeRechercheControleur import YoutubeRechercheControleur
from modele.audio.AudioModele import AudioModele
from modele.bluetooth.BluetoothModele import BluetoothModele
from modele.lecteur.BibliothequeSpotifyModele import BibliothequeSpotifyModele
from modele.lecteur.JukeBoxModele import JukeBoxModele, Ecran
from modele.lecteur.ListeLectureModele import ListeLectureModele
from modele.wifi.WifiModele import WifiModele
from service.bluetooth.BluetoothService import BluetoothService
from service.ErreurService import ErreurService
from minitel.Minitel import Minitel
from service.minitel.MinitelExtension import MinitelExtension
from service.minitel.MinitelConstante import TOUCHE_ECHAP, TOUCHE_SHIFT_ENTREE
from service.wifi.WifiService import WifiService
from vue.bidule.Sablier import Sablier
from vue.ecran.EcranBibliothequeSpotify import EcranBibliothequeSpotify
from vue.ecran.EcranBluetooth import EcranBluetooth
from vue.ecran.EcranDemarrage import EcranDemarrage
from vue.ecran.EcranFinVue import EcranFinVue
from vue.ecran.EcranListeLecture import EcranListeLecture
from vue.ecran.EcranRecherche import EcranRecherche
from vue.ecran.EcranVisualisation import EcranVisualisation


class JukeBoxControleur(PeutGererTouche):
    __sablier = inject.attr(Sablier)

    @inject.autoparams()
    def __init__(self, bluetooth_service: BluetoothService, audio_modele: AudioModele,
                 lecteur_controleur: LecteurControleur, liste_lecture_modele: ListeLectureModele):
        logging.debug("Initialisation du JukeBox")
        self.__jukebox_modele = JukeBoxModele()

        wifi_modele = WifiModele()
        wifi_service = WifiService()
        try:
            wifi_modele.wifi = wifi_service.recuperer_wifi()
        except Exception as erreur:
            wifi_modele.wifi = None
            ErreurService.signaler("Lecture de l'etat Wi-Fi au demarrage", erreur)

        bluetooth_modele = BluetoothModele()

        self.__titre_controleur = TitreControleur(bluetooth_modele, bluetooth_service, wifi_modele, wifi_service)
        audio_controleur = AudioControleur(audio_modele)

        self.__mvc_createur = MVCCreateur(
            {"audio": audio_controleur, "lecteur": lecteur_controleur, "jukebox": self},
            {"jukebox": self.__jukebox_modele, "bluetooth": bluetooth_modele, "wifi": wifi_modele,
             "liste_lecture": liste_lecture_modele}
        )

    def demarrer(self):
        logging.info(f"Démarrage du JukeBox")
        EcranDemarrage().afficher()

        while not self.__jukebox_modele.est_termine():
            ecran = self.__jukebox_modele.ecran_demande
            try:
                self.__lancer_ecran()
            except Exception as erreur:
                message = ErreurService.signaler(
                    f"Chargement du mode {ecran.name if ecran else 'inconnu'}", erreur)
                self.__jukebox_modele.ecran_courant = ecran
                self.__ecran_erreur(message)

        EcranFinVue().afficher()
        self.fermer()

    def __ecran_erreur(self, message=None):
        minitel = inject.instance(Minitel)
        extension = inject.instance(MinitelExtension)
        minitel.efface('vraimenttout')
        message = message or ErreurService.recuperer() or "Le mode demande n'a pas pu etre charge."
        extension.envoyer_ligne(posy=3, texte="Erreur de chargement", couleur="rouge")
        for index, ligne in enumerate(textwrap.wrap(message, width=39)[:8], start=4):
            extension.envoyer_ligne(posy=index, texte=ligne, couleur="rouge")
        extension.envoyer_ligne(posy=13, texte="SOMMAIRE: passer a un autre ecran", couleur="jaune")
        while not self.__jukebox_modele.est_termine():
            touche = minitel.recevoir_sequence(bloque=True, attente=None)
            if self.gere_touche(touche):
                break

    def __lancer_ecran(self):
        if self.__jukebox_modele.ecran_demande == Ecran.ECRAN_BLUETOOTH:
            bluetooth_controleur = self.__mvc_createur.creation(BluetoothControleur, EcranBluetooth, {})
            bluetooth_controleur.lancer()
        elif self.__jukebox_modele.ecran_demande == Ecran.ECRAN_RECHERCHE:
            recherche_controller = self.__mvc_createur.creation(YoutubeRechercheControleur, EcranRecherche, {})
            recherche_controller.lancer()
        elif self.__jukebox_modele.ecran_demande == Ecran.ECRAN_VISUALISATION:
            visualisation_controller = self.__mvc_createur.creation(AbstractControleur, EcranVisualisation, {})
            visualisation_controller.lancer()
        elif self.__jukebox_modele.ecran_demande == Ecran.ECRAN_LISTE_LECTURE:
            liste_lecture_controller = self.__mvc_createur.creation(AbstractControleur, EcranListeLecture, {})
            liste_lecture_controller.lancer()
        elif self.__jukebox_modele.ecran_demande == Ecran.ECRAN_BIBLIOTHEQUE_SPOTIFY:
            bibliotheque_spotify_controller = self.__mvc_createur.creation(
                BibliothequeSpotifyControleur, EcranBibliothequeSpotify, {"spotify": BibliothequeSpotifyModele()})
            bibliotheque_spotify_controller.lancer()
        else:
            raise ValueError(f"Mode inconnu: {self.__jukebox_modele.ecran_demande}")

    def gere_touche(self, touche: Sequence) -> Optional[bool]:
        logging.debug(f"Gestion de la touche par le jukebox {touche.valeurs}")
        if touche.egale(TOUCHE_ECHAP):
            self.__jukebox_modele.arreter_jukebox()
            return True

        if touche.egale(SOMMAIRE):
            logging.info("Sommaire de la boucle principale du JukeBox")
            if self.__jukebox_modele.ecran_courant == Ecran.ECRAN_RECHERCHE:
                self.__jukebox_modele.ecran_demande = Ecran.ECRAN_BIBLIOTHEQUE_SPOTIFY
                return True
            elif self.__jukebox_modele.ecran_courant == Ecran.ECRAN_BIBLIOTHEQUE_SPOTIFY:
                self.__jukebox_modele.ecran_demande = Ecran.ECRAN_VISUALISATION
                return True
            else:
                self.__jukebox_modele.ecran_demande = Ecran.ECRAN_RECHERCHE
                return True

        if touche.egale(TOUCHE_SHIFT_ENTREE):
            logging.info("Shift+Sommaire de la boucle principale du JukeBox")
            self.__jukebox_modele.ecran_demande = Ecran.ECRAN_LISTE_LECTURE
            return True

        return None

    def fermer(self):
        logging.info(f"Fermeture du JukeBox")
        self.__sablier.detruire()
        self.__titre_controleur.arreter()
