__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import inject
from pyobservable import Observable

from service.LecteurService import LecteurService


class LecteurModele:
    EVENEMENT_RECHERCHE_CHANSON = "RechercheChanson"
    EVENEMENT_CHANGEMENT_CHANSON = "ChangementChanson"
    EVENEMENT_PAUSE = "Pause"
    EVENEMENT_REPRISE = "Reprise"

    @inject.autoparams()
    def __init__(self, lecteur_service: LecteurService, notificateur_evenement: Observable):
        self.__lecteur_service = lecteur_service
        self.__notificateur_evenement = notificateur_evenement
        self.__chanson_courante = None

    def jouer_chanson(self, nom_chanson):
        self.__notificateur_evenement.notify(LecteurModele.EVENEMENT_RECHERCHE_CHANSON, nom_chanson)
        chanson_trouvee = self.__lecteur_service.rechercher_chanson(nom_chanson, 1)[0]

        self.__notificateur_evenement.notify(LecteurModele.EVENEMENT_CHANGEMENT_CHANSON, chanson_trouvee["titre"])
        self.__lecteur_service.jouer_url(chanson_trouvee["url"])

        self.__chanson_courante = chanson_trouvee

    def pause_ou_reprendre(self):
        retour = self.__lecteur_service.pause_ou_reprendre()
        if retour is None:
            return
        if retour is True:
            self.__notificateur_evenement.notify(LecteurModele.EVENEMENT_REPRISE, self.__chanson_courante["titre"])
        if retour is False:
            self.__notificateur_evenement.notify(LecteurModele.EVENEMENT_PAUSE, self.__chanson_courante["titre"])
