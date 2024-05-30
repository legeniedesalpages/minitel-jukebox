__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from typing import Optional

import inject
from minitel.Minitel import Minitel
from minitel.Sequence import Sequence
from minitel.constantes import SOMMAIRE

from configuration.MVCCreateur import MVCCreateur
from controleur.BluetoothControleur import BluetoothControleur
from controleur.PeutGererTouche import PeutGererTouche
from controleur.composant.AudioControleur import AudioControleur
from controleur.composant.LectureControleur import LectureControleur
from controleur.composant.TitreControleur import TitreControleur
from controleur.recherche.RechercheControleur import RechercheControleur
from modele.BluetoothModele import BluetoothModele
from modele.JukeBoxModele import JukeBoxModele
from service.BluetoothService import BluetoothService
from service.minitel.MinitelConstante import TOUCHE_ECHAP
from vue.EcranBluetooth import EcranBluetooth
from vue.bidule.Sablier import Sablier
from vue.recherche.EcranRecherche import EcranRecherche


class JukeBoxControleur(PeutGererTouche):
    __sablier = inject.attr(Sablier)

    @inject.autoparams()
    def __init__(self, mvc_createur: MVCCreateur, jukebox_modele: JukeBoxModele, bluetooth_modele: BluetoothModele, bluetooth_service: BluetoothService, minitel: Minitel):
        logging.debug("Initialisation du JukeBox")
        self.__jukebox_modele = jukebox_modele
        self.__bluetooth_modele = bluetooth_modele
        self.__titre_controleur = TitreControleur(self.__bluetooth_modele, bluetooth_service)
        self.__mvc_createur = mvc_createur

    def demarrer(self):
        logging.info(f"Démarrage du JukeBox")
        audio_controleur = AudioControleur()
        lecture_controleur = LectureControleur()
        self.__mvc_createur.ajouter_controleur_commun([self, audio_controleur, lecture_controleur])
        self.__mvc_createur.ajouter_modele_commun({"jukebox": self.__jukebox_modele, "bluetooth": self.__bluetooth_modele})
        # EcranDemarrageVue().afficher()

        bluetooth_controleur = self.__mvc_createur.creation(BluetoothControleur, EcranBluetooth, {})
        bluetooth_controleur.lancer()

        while not self.__jukebox_modele.est_termine():
            recherche_controller = self.__mvc_createur.creation(RechercheControleur, EcranRecherche, {})
            recherche_controller.lancer()

        self.fermer()

    def gere_touche(self, touche: Sequence) -> Optional[bool]:
        if touche.egale(TOUCHE_ECHAP):
            self.__jukebox_modele.arreter_jukebox()
            return True

        if touche.egale(SOMMAIRE):
            logging.info("Sommaire de la boucle principale du JukeBox")
            return True

        return None

    def fermer(self):
        logging.info(f"Fermeture du JukeBox")
        self.__sablier.detruire()
        self.__titre_controleur.arreter()
