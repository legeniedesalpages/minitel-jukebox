__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import importlib
from typing import Type

from controleur.commun.AbstractControleur import AbstractControleur
from controleur.commun.PeutGererTouche import PeutGererTouche
from vue.commun.AbstractEcran import AbstractEcran


class MVCCreateur:

    def __init__(self, controleur_pouvant_gerer_touche: dict[str, PeutGererTouche], modeles: dict[str, object]):
        self.__controleurs_pouvant_gerer_touche = controleur_pouvant_gerer_touche
        self.__modeles_communs = modeles

    def creation(self, controleur_type: Type[AbstractControleur], vue_type: Type[AbstractEcran],
                 map_modele: dict[str, object]) -> AbstractControleur:
        modeles = map_modele | self.__modeles_communs

        controleur: AbstractControleur = self.__instanciation(controleur_type)(
            self.__controleurs_pouvant_gerer_touche,
            modeles
        )

        vue: AbstractEcran = self.__instanciation(vue_type)(
            controleur,
            modeles
        )

        controleur.enregistrer_vue(vue)

        return controleur

    @staticmethod
    def __instanciation(class_type):
        module_name, class_name = class_type.__module__.rsplit(".", 1)
        lib = importlib.import_module(class_type.__module__)
        return getattr(lib, class_name)
