__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import abc
import logging
import textwrap
from queue import Empty

import inject
from minitel.Minitel import Minitel
from minitel.Sequence import Sequence
from pyobservable import Observable

from controleur.commun.AbstractControleur import AbstractControleur
from modele.bluetooth.BluetoothModele import BluetoothModele
from modele.lecteur.ListeLectureModele import ListeLectureModele
from modele.wifi.WifiModele import WifiModele
from service.ErreurService import ErreurService
from minitel.constantes import SOMMAIRE
from service.minitel.MinitelExtension import MinitelExtension
from service.minitel.MinitelConstante import TOUCHE_ECHAP, TOUCHE_SHIFT_ENTREE
from vue.bidule.Sablier import Sablier
from vue.commun.Affichable import Affichable
from vue.composant.BarreAudioVue import BarreAudioVue
from vue.composant.BarreLectureVue import BarreLectureVue
from vue.composant.BarreTitreVue import BarreTitreVue


class AbstractEcran(Affichable):
    __metaclass__ = abc.ABCMeta

    _sablier = inject.attr(Sablier)
    _notificateur_evenement = inject.attr(Observable)
    _minitel: Minitel = inject.attr(Minitel)
    _minitel_extension: MinitelExtension = inject.attr(MinitelExtension)

    __barre_titre_vue: BarreTitreVue
    __barre_lecture: BarreLectureVue

    __bluetooth_modele: BluetoothModele
    __wifi_modele: WifiModele
    __liste_lecture_modele: ListeLectureModele

    _controleur: AbstractControleur

    def __init__(self, controleur: AbstractControleur, modeles: dict[str, object]):
        logging.debug("Init vue générique")
        self._controleur = controleur

        # noinspection PyTypeChecker
        self.__bluetooth_modele = modeles["bluetooth"]
        # noinspection PyTypeChecker
        self.__wifi_modele = modeles["wifi"]
        # noinspection PyTypeChecker
        self.__liste_lecture_modele = modeles["liste_lecture"]

        self.__barre_audio_vue = BarreAudioVue(self._get_callback_curseur)

    def afficher(self):
        logging.debug("Affichage vue")
        self.__erreur_visible = False
        self.__barre_titre_vue = BarreTitreVue(self._get_titre_ecran(), self.__bluetooth_modele, self.__wifi_modele, self._get_callback_curseur)
        self.__barre_lecture = BarreLectureVue(self.__liste_lecture_modele, self._get_callback_curseur)
        try:
            try:
                self.__barre_titre_vue.afficher()
                self._affichage_initial()
                self.__barre_lecture.afficher()
            except Exception as erreur:
                ErreurService.signaler(f"Ouverture de {self._get_titre_ecran()}", erreur)
                self.__erreur_visible = True

            while True:
                erreur = ErreurService.recuperer()
                if erreur is not None:
                    self.__afficher_erreur(erreur)
                touche = self.__recupere_sequence()
                if touche.longueur == 0:
                    continue
                try:
                    # La navigation reste accessible meme si le contenu de l'ecran est inutilisable.
                    if touche.egale(SOMMAIRE) or (self.__erreur_visible and (
                            touche.egale(TOUCHE_ECHAP) or touche.egale(TOUCHE_SHIFT_ENTREE))):
                        if self.__erreur_visible:
                            quitter = any(
                                controleur.gere_touche(touche)
                                for controleur in self._controleur._controleur_pouvant_gerer_touche)
                        else:
                            quitter = self._controleur.gere_touche(touche)
                        if quitter:
                            break
                    elif not self.__erreur_visible and not self._gere_touche(touche):
                        if self._controleur.gere_touche(touche):
                            break
                except Exception as erreur:
                    ErreurService.signaler(f"Action dans {self._get_titre_ecran()}", erreur)
                    self.__erreur_visible = True
        finally:
            self.__fermer()
            self._minitel.efface('vraimenttout')

    def __afficher_erreur(self, message: str):
        self.__erreur_visible = True
        self._sablier.arreter()
        self._minitel_extension.envoyer_ligne(posy=3, texte="Erreur - action interrompue", couleur="rouge")
        for ligne in range(4, 12):
            self._minitel_extension.envoyer_ligne(posy=ligne, texte="")
        for index, ligne in enumerate(textwrap.wrap(message, width=39)[:8], start=4):
            self._minitel_extension.envoyer_ligne(posy=index, texte=ligne, couleur="rouge")
        self._minitel_extension.envoyer_ligne(
            posy=13, texte="SOMMAIRE: passer a un autre ecran", couleur="jaune")

    def __fermer(self):
        for fermeture in (self.__barre_audio_vue.fermer, self.__barre_titre_vue.fermer,
                          self.__barre_lecture.fermer, self.fermer):
            try:
                fermeture()
            except Exception as erreur:
                ErreurService.signaler("Fermeture d'un composant de l'ecran", erreur)

    def __recupere_sequence(self) -> Sequence:
        try:
            return self._minitel.recevoir_sequence(bloque=True, attente=0.2)
        except Empty:
            return Sequence()

    @abc.abstractmethod
    def _affichage_initial(self):
        logging.debug("Affichage initial de l'écran générique")

    @abc.abstractmethod
    def _get_titre_ecran(self) -> str:
        return "Ecran générique"

    @abc.abstractmethod
    def _get_callback_curseur(self):
        logging.info("Callback curseur générique")

    @abc.abstractmethod
    def _gere_touche(self, touche: Sequence) -> bool:
        return False

    @abc.abstractmethod
    def fermer(self):
        logging.info("Fermeture de l'écran générique")
