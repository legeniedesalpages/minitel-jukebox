__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from pyobservable import Observable

from modele.audio.AudioModele import AudioModele
from modele.bluetooth.BluetoothModele import BluetoothModele
from modele.lecteur.JukeBoxModele import JukeBoxModele
from modele.lecteur.ListeLectureModele import ListeLectureModele
from modele.wifi.WifiModele import WifiModele
from vue.bidule.Liste import Liste


def produire_notificateur_evenement() -> Observable:
    notificateur_evenement = Observable()

    notificateur_evenement.add_event(AudioModele.EVENEMENT_CHANGEMENT_VOLUME)

    notificateur_evenement.add_event(BluetoothModele.EVENEMENT_LISTE_PERIPHERIQUE_BLUETOOTH_CHANGE)
    notificateur_evenement.add_event(BluetoothModele.EVENEMENT_PERIPHERIQUE_BLUETOOTH_APAIRE_CHANGE)
    notificateur_evenement.add_event(BluetoothModele.EVENEMENT_SELECTION_DANS_LISTE_PERIPHERIQUE_CHANGE)

    notificateur_evenement.add_event(WifiModele.EVENEMENT_WIFI_CHANGE)

    notificateur_evenement.add_event(Liste.EVENEMENT_LISTE_CHANGE_PAGE)

    notificateur_evenement.add_event(JukeBoxModele.EVENEMENT_NOTIFICATION)

    notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_STOP)
    notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_PROGRESSE)
    notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_JOUE)
    notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_PAUSE)
    notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_CHARGEMENT)
    notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_CHANGE_CHANSON)

    return notificateur_evenement
