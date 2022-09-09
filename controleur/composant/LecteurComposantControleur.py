__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject

from modele.composant.LecteurModele import LecteurModele
from service.ChansonService import ChansonService


class LecteurComposantControleur:

    @inject.autoparams()
    def __init__(self, lecteur_modele: LecteurModele, chanson_service: ChansonService):
        logging.debug("Initialisation UI Contrôleur")
        self.__lecteur_modele = lecteur_modele
        self.__chanson_service = chanson_service

    def action_repeter_chanson(self):
        logging.debug("Repeter chanson")
        self.__lecteur_modele.repeter_chanson()

    def action_pause_ou_reprendre(self):
        logging.debug("Mise en pause ou reprise")
        self.__lecteur_modele.pause_ou_reprendre()

    def action_lire_chanson(self):
        logging.debug("Lire chanson")
        liste_chanson = self.__chanson_service.rechercher_chanson("mon reve bleu", 1)
        self.__lecteur_modele.lire_chanson(liste_chanson[0])

    def action_chanson_suivante(self):
        logging.debug("Recherche de la chanson suivante")
        chanson = self.__chanson_service.suggestion(self.__lecteur_modele.chanson_courante.titre)
        logging.info(f"Chanson suivante trouvée: {chanson}")
        liste_chanson = self.__chanson_service.rechercher_chanson(chanson, 1)
        self.__lecteur_modele.lire_chanson(liste_chanson[0])
