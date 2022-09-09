__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject

from modele.RechercheModele import RechercheModele


class RechercheControleur:

    @inject.autoparams()
    def __init__(self, recherche_modele: RechercheModele):
        # privé
        self.__recherche_modele = recherche_modele

    def lancer_recherche(self, chanson_a_chercher):
        logging.info(f"Lancement de la recherche pour: {chanson_a_chercher}")
        self.__recherche_modele.lancer_recherche(chanson_a_chercher)
