__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import inject

from controleur.ComposantControleur import ComposantControleur
from modele.RechercheModele import RechercheModele


class RechercheControleur:

    @inject.autoparams()
    def __init__(self, recherche_modele: RechercheModele, composant_controleur: ComposantControleur):
        # public
        self.composant_controleur = composant_controleur
        # privé
        self.__recherche_modele = recherche_modele

    def afficher_ecran_recherche(self):
        self.__recherche_modele.affichage_ecran_recherche()
