__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from pyobservable import Observable

from modele.BluetoothModele import BluetoothModele
from modele.audio.AudioModele import AudioModele


def produire_notificateur_evenement() -> Observable:
    notificateur_evenement = Observable()

    notificateur_evenement.add_event(AudioModele.EVENEMENT_CHANGEMENT_VOLUME)

    notificateur_evenement.add_event(BluetoothModele.EVENEMENT_LISTE_PERIPHERIQUE_BLUETOOTH_CHANGE)
    notificateur_evenement.add_event(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE)
    notificateur_evenement.add_event(BluetoothModele.EVENEMENT_SELECTION_DANS_LISTE_PERIPHERIQUE_CHANGE)

    return notificateur_evenement
