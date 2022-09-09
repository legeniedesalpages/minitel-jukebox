__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
from enum import Enum

import inject
from pyobservable import Observable

from modele.Chanson import Chanson
from service.ChansonService import ChansonService
from service.LecteurService import LecteurService


class EvenementLecteurModele(Enum):
    EVENEMENT_ARRET = "EvenementArret"
    EVENEMENT_CHARGEMENT_CHANSON = "EvenementChargementChanson"
    EVENEMENT_LECTURE = "EvenementLecture"
    EVENEMENT_AVANCEMENT_LECTURE = "EvenementAvancementLecture"
    EVENEMENT_PAUSE = "EvenementPause"
    EVENEMENT_FIN_CHANSON = "EvenementFinChanson"


class EtatLecteur(Enum):
    CHARGEMENT_CHANSON = "ChargementChanson"
    ARRET = "EtatArret"
    LECTURE = "EtatLecture"
    PAUSE = "EtatPause"


class LecteurModele:

    @inject.autoparams()
    def __init__(self, lecteur_service: LecteurService, chanson_service: ChansonService,
                 notificateur_evenement: Observable):
        # services
        self.__lecteur_service = lecteur_service
        self.__chanson_service = chanson_service
        self.__notificateur_evenement = notificateur_evenement
        self.__lecteur_service.enregistrer_callback(self.callback_vlc)
        # propriétés interne
        self.chanson_courante = None
        self.__etat = EtatLecteur.ARRET

    def recuperer_etat(self) -> EtatLecteur:
        return self.__etat

    def recuperer_chanson(self) -> Chanson:
        return self.chanson_courante

    def lire_chanson(self, chanson: Chanson):
        self.__lecteur_service.arreter_lecture()
        self.__lecteur_service.jouer_url(chanson.url_stream)
        self.chanson_courante = chanson

    def repeter_chanson(self):
        if self.chanson_courante is not None:
            self.lire_chanson(self.chanson_courante)
        else:
            logging.info("Pas de chanson courante à répéter")

    def chanson_suivante(self):
        logging.debug("Chanson suivante")
        if self.chanson_courante is not None:
            chanson = self.__chanson_service.suggestion(self.chanson_courante.titre)
            logging.info(f"Chanson suivante trouvée: {chanson}")
            liste_chanson = self.__chanson_service.rechercher_chanson(chanson, 1)
            self.__lecteur_service.jouer_url(liste_chanson[0].url_stream)
            self.chanson_courante = chanson
        else:
            logging.info("Pas de chanson suivante car pas de chanson courante")

    def callback_vlc(self, evenement, valeur):
        if evenement is not LecteurService.EVENEMENT_AVANCEMENT:
            logging.debug(f"Callback Event VLC : {evenement}, {valeur}")

        if self.chanson_courante is not None:
            titre = self.chanson_courante.titre
        else:
            titre = ""

        if evenement == LecteurService.EVENEMENT_PAUSE:
            self.__etat = EtatLecteur.PAUSE
            self.__notificateur_evenement.notify(EvenementLecteurModele.EVENEMENT_PAUSE, titre)
        elif evenement == LecteurService.EVENEMENT_LECTURE:
            self.__etat = EtatLecteur.LECTURE
            self.__notificateur_evenement.notify(EvenementLecteurModele.EVENEMENT_LECTURE, titre)
        elif evenement == LecteurService.EVENEMENT_AVANCEMENT:
            self.__etat = EtatLecteur.LECTURE
            self.__notificateur_evenement.notify(EvenementLecteurModele.EVENEMENT_AVANCEMENT_LECTURE, valeur)
        elif evenement == LecteurService.EVENEMENT_ARRET:
            self.__etat = EtatLecteur.ARRET
            self.__notificateur_evenement.notify(EvenementLecteurModele.EVENEMENT_ARRET, titre)
        elif evenement == LecteurService.EVENEMENT_CHARGEMENT:
            self.__etat = EtatLecteur.CHARGEMENT_CHANSON
            self.__notificateur_evenement.notify(EvenementLecteurModele.EVENEMENT_CHARGEMENT_CHANSON, titre)
        elif evenement == LecteurService.EVENEMENT_FIN_CHANSON:
            self.__notificateur_evenement.notify(EvenementLecteurModele.EVENEMENT_FIN_CHANSON, titre)

    def pause_ou_reprendre(self):
        self.__lecteur_service.pause_ou_reprendre()
