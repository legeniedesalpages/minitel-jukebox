__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from pyobservable import Observable

from modele.AudioModele import AudioModele
from modele.LecteurModele import LecteurModele
from modele.RechercheModele import RechercheModele


def produire_notificateur_evenement() -> Observable:
    notificateur_evenement = Observable()

    notificateur_evenement.add_event(AudioModele.EVENEMENT_CHANGEMENT_VOLUME)

    notificateur_evenement.add_event(LecteurModele.EVENEMENT_RECHERCHE_CHANSON)
    notificateur_evenement.add_event(LecteurModele.EVENEMENT_CHANGEMENT_CHANSON)
    notificateur_evenement.add_event(LecteurModele.EVENEMENT_PAUSE)
    notificateur_evenement.add_event(LecteurModele.EVENEMENT_REPRISE)

    notificateur_evenement.add_event(RechercheModele.EVENEMENT_RECHERCHE_AFFICHAGE)

    return notificateur_evenement
