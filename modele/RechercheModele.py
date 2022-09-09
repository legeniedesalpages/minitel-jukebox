__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import inject
from pyobservable import Observable

from service.LecteurService import LecteurService


class RechercheModele:

    @inject.autoparams()
    def __init__(self, lecteur_service: LecteurService, notificateur_evenement: Observable):
        self.__notificateur_evenement = notificateur_evenement
        self.__lecteur_service = lecteur_service

    def lancer_recherche(self, chanson_a_chercher):
        self.__lecteur_service.rechercher_chanson(chanson_a_chercher)
