__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import abc
import logging
from queue import Empty

import inject
from minitel.Minitel import Minitel
from minitel.Sequence import Sequence
from pyobservable import Observable

from controleur.AbstractControleur import AbstractControleur
from modele.BluetoothModele import BluetoothModele
from modele.ListeLectureModele import ListeLectureModele
from modele.wifi.WifiModele import WifiModele
from service.minitel.MinitelExtension import MinitelExtension
from vue.Affichable import Affichable
from vue.bidule.Sablier import Sablier
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

        self.__barre_titre_vue = BarreTitreVue(self._get_titre_ecran(), self.__bluetooth_modele, self.__wifi_modele, self._get_callback_curseur)
        self.__barre_titre_vue.afficher()

        self._affichage_initial()

        self.__barre_lecture = BarreLectureVue(self.__liste_lecture_modele, self._get_callback_curseur)
        self.__barre_lecture.afficher()

        while True:
            touche = self.__recupere_sequence()
            logging.debug(f"Touche {touche.valeurs}")

            if touche.longueur > 0:
                if not self._gere_touche(touche):
                    if self._controleur.gere_touche(touche):
                        break

        self._minitel.efface('vraimenttout')
        self.__fermer()

    def __fermer(self):
        self.__barre_audio_vue.fermer()
        self.__barre_titre_vue.fermer()
        self.__barre_lecture.fermer()
        self.fermer()

    def __recupere_sequence(self) -> Sequence:
        try:
            return self._minitel.recevoir_sequence(bloque=True, attente=None)
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
