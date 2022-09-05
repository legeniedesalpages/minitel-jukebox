__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import inject
from pyobservable import Observable


class RechercheModele:
    EVENEMENT_RECHERCHE_AFFICHAGE = "AffichageRecherche"

    @inject.autoparams()
    def __init__(self, notificateur_evenement: Observable):
        self.__notificateur_evenement = notificateur_evenement

    def affichage_ecran_recherche(self):
        self.__notificateur_evenement.notify(RechercheModele.EVENEMENT_RECHERCHE_AFFICHAGE)
