__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from pyobservable import Observable

from modele.composant.AudioModele import AudioModele
from modele.recherche.AbstractRechercheModele import AbstractRechercheModele


def produire_notificateur_evenement() -> Observable:
    notificateur_evenement = Observable()

    notificateur_evenement.add_event(AudioModele.EVENEMENT_CHANGEMENT_VOLUME)

    notificateur_evenement.add_event(AbstractRechercheModele.EVENEMENT_CHANGEMENT_RESULTAT)
    notificateur_evenement.add_event(AbstractRechercheModele.EVENEMENT_CHANGEMENT_SELECTION)

    return notificateur_evenement
