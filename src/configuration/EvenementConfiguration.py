__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from pyobservable import Observable

from modele.audio.AudioModele import AudioModele


# from modele.recherche.AbstractRechercheModele import EvenementRechercheModele


def produire_notificateur_evenement() -> Observable:
    notificateur_evenement = Observable()

    notificateur_evenement.add_event(AudioModele.EVENEMENT_CHANGEMENT_VOLUME)

    # for evenement_recherche_modele in EvenementRechercheModele:
    #     notificateur_evenement.add_event(evenement_recherche_modele)

    return notificateur_evenement
