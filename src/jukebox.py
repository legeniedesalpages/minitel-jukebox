__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
from minitel.Minitel import Minitel
from pyobservable import Observable

from configuration.EvenementConfiguration import produire_notificateur_evenement
from controleur.JukeBoxControleur import JukeBoxControleur
from controleur.composant.LecteurControleur import LecteurControleur
from modele.ListeLectureModele import ListeLectureModele
from service.VlcService import VlcService
from service.minitel.MinitelConfiguration import produire_minitel


def jukebox_inject_config(binder):
    logging.debug("Configuration de l'injecteur de dépendance")
    binder.bind(Minitel, produire_minitel())
    binder.bind(Observable, produire_notificateur_evenement())
    liste_lecture_modele = ListeLectureModele()
    binder.bind(ListeLectureModele, liste_lecture_modele)
    lecteur_controleur = LecteurControleur(liste_lecture_modele)
    binder.bind(LecteurControleur, lecteur_controleur)
    vlc_service = VlcService(lecteur_controleur)
    binder.bind(VlcService, vlc_service)


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(levelname)-5s] %(filename)s:%(lineno)d -> %(message)s"
    )

    logging.info("Lancement du Jukebox Minitel")
    inject.configure(jukebox_inject_config)

    juke_box = JukeBoxControleur()
    try:
        juke_box.demarrer()
    except KeyboardInterrupt:
        juke_box.fermer()
        pass

    logging.info("Arret du Jukebox Minitel")
