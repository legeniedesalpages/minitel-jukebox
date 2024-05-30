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
from vue.Affichable import Affichable
from vue.bidule.Sablier import Sablier
from vue.composant.BarreTitreVue import BarreTitreVue


class AbstractEcran(Affichable):
    __metaclass__ = abc.ABCMeta

    __sablier = inject.attr(Sablier)
    __notificateur_evenement = inject.attr(Observable)

    _minitel: Minitel
    _controleur: AbstractControleur
    __barre_titre_vue: BarreTitreVue
    __bluetooth_modele: BluetoothModele

    def __init__(self, minitel: Minitel, controleur: AbstractControleur, modeles: dict[str, object]):
        logging.debug("Init vue générique")
        self._minitel = minitel
        self._controleur = controleur
        # noinspection PyTypeChecker
        self.__bluetooth_modele = modeles["bluetooth"]

    def afficher(self):
        logging.debug("Affichage vue")

        self.__barre_titre_vue = BarreTitreVue(self._minitel, self._get_titre_ecran(), self.__bluetooth_modele)
        self.__barre_titre_vue.afficher()
        self._affichage_initial()

        sequence = self.__recupere_sequence()
        while True:
            logging.debug(f"Touche {sequence.valeurs}")

            if sequence.longueur > 0:
                if self._controleur.gere_touche(sequence):
                    break

            # on se remet en attente de la prochaine touche
            sequence = self.__recupere_sequence()

        self._minitel.efface('vraimenttout')
        self.__fermer()

    def __fermer(self):
        self.__barre_titre_vue.fermer()
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
    def fermer(self):
        logging.info("Fermeture de l'écran générique")
