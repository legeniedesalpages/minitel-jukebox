__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-06-04"
__version__ = "1.0.0"

import logging
import unittest
from unittest.mock import Mock, call

import inject
from minitel.Minitel import Minitel
from pyobservable import Observable

from modele.lecteur.Chanson import Chanson
from modele.lecteur.ListeLectureModele import ListeLectureModele, EtatLecture
from service.minitel.MinitelExtension import MinitelExtension
from vue.composant.BarreLectureVue import BarreLectureVue


class BarreLectureVueTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)-5s] %(filename)s:%(lineno)d -> %(message)s"
        )

    def test_doit_gerer_le_pourcentage_correctement(self):
        notificateur_evenement = Observable()
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_STOP)
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_JOUE)
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_PAUSE)
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_PROGRESSE)
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_CHANGE_CHANSON)
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_CHARGEMENT)

        minitel = Mock()

        inject.configure(lambda binder:
                         binder.bind(Observable, notificateur_evenement).
                         bind(Minitel, minitel).
                         bind(MinitelExtension, Mock())
                         )

        def callback():
            pass

        liste_lecture_modele = ListeLectureModele(Mock())
        barre_lecture = BarreLectureVue(liste_lecture_modele, callback)
        barre_lecture.afficher()
        calls = [call('S'), call('|'), call(' ' * 35), call('|   ')]
        minitel.envoyer.assert_has_calls(calls, any_order=False)

        calls += [call('|50%')]
        liste_lecture_modele.progression_chanson_courante = 50
        notificateur_evenement.notify(ListeLectureModele.EVENEMENT_LECTURE_PROGRESSE)
        minitel.envoyer.assert_has_calls(calls, any_order=False)

        calls += [call('| 0%')]
        liste_lecture_modele.progression_chanson_courante = 0
        notificateur_evenement.notify(ListeLectureModele.EVENEMENT_LECTURE_PROGRESSE)
        minitel.envoyer.assert_has_calls(calls, any_order=False)

        calls += [call('|fin')]
        liste_lecture_modele.progression_chanson_courante = 100
        notificateur_evenement.notify(ListeLectureModele.EVENEMENT_LECTURE_PROGRESSE)
        minitel.envoyer.assert_has_calls(calls, any_order=False)

        calls += [call('S'), call('|')]
        liste_lecture_modele.etat_lecture = EtatLecture.STOP
        notificateur_evenement.notify(ListeLectureModele.EVENEMENT_LECTURE_STOP)
        minitel.envoyer.assert_has_calls(calls, any_order=False)

        calls += [call('P'), call('|')]
        liste_lecture_modele.etat_lecture = EtatLecture.PAUSE
        notificateur_evenement.notify(ListeLectureModele.EVENEMENT_LECTURE_PAUSE)
        minitel.envoyer.assert_has_calls(calls, any_order=False)

        calls += [call('L'), call('|')]
        liste_lecture_modele.etat_lecture = EtatLecture.JOUE
        notificateur_evenement.notify(ListeLectureModele.EVENEMENT_LECTURE_JOUE)
        minitel.envoyer.assert_has_calls(calls, any_order=False)

        calls += [call('12345678901234567890123456789012345')]
        liste_lecture_modele.ajouter_chanson(Chanson("1", "12345678901234567890123456789012345678901234567890", "01:00", "http://image/1"))
        notificateur_evenement.notify(ListeLectureModele.EVENEMENT_LECTURE_CHANGE_CHANSON)
        minitel.envoyer.assert_has_calls(calls, any_order=False)

        calls += [call('12345                              ')]
        liste_lecture_modele.inserer_puis_jouer_chanson(Chanson("1", "12345", "01:00", "http://image/1"), Mock())
        notificateur_evenement.notify(ListeLectureModele.EVENEMENT_LECTURE_CHANGE_CHANSON)
        minitel.envoyer.assert_has_calls(calls, any_order=False)




