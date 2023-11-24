__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import importlib
from typing import Type, List, Tuple

import inject
from minitel.Minitel import Minitel

from controleur.AbstractControleur import AbstractControleur
from service.minitel.MinitelExtension import MinitelExtension
from vue.AbstractVue import AbstractVue


class MVCCreateur:

    @inject.autoparams()
    def __init__(self, minitel: Minitel, minitel_extension: MinitelExtension):
        self.__minitel = minitel
        self.__minitel_extension = minitel_extension

    def creation(self, controleur_type: Type[AbstractControleur], vue_type: Type[AbstractVue], liste_modele: List) -> \
            Tuple[AbstractControleur, AbstractVue]:
        controleur: AbstractControleur = self.__instanciation(controleur_type)(
            self.__minitel,
            liste_modele
        )

        vue: AbstractVue = self.__instanciation(vue_type)(
            self.__minitel,
            self.__minitel_extension,
            controleur,
            liste_modele
        )

        controleur.enregistrer_vue(vue)

        return controleur, vue

    @staticmethod
    def __instanciation(class_type):
        module_name, class_name = class_type.__module__.rsplit(".", 1)
        lib = importlib.import_module(class_type.__module__)
        return getattr(lib, class_name)
