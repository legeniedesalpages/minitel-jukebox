__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
import unittest
from unittest.mock import Mock

from pyobservable import Observable

from modele.lecteur.Chanson import Chanson
from modele.lecteur.ListeLectureModele import ListeLectureModele, EtatLecture
from service.lecteur.AbstractLecteurService import AbstractLecteurService


class ListeLectureModeleTest(unittest.TestCase):
    chanson_1: Chanson
    chanson_2: Chanson
    chanson_3: Chanson

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)-5s] %(filename)s:%(lineno)d -> %(message)s"
        )

    def setUp(self):
        self.chanson_1 = Chanson("1", "un", "01:00", "http://image/1")
        self.chanson_2 = Chanson("2", "deux", "02:00", "http://image/2")
        self.chanson_3 = Chanson("3", "trois", "03:00", "http://image/3")
        self.chanson_1_5 = Chanson("1.5", "un point cinq", "04:00", "http://image/1/5")

    def test_doit_recuperer_chanson_lecture_simple_sans_repetition(self):
        notificateur_evenement = Observable()
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_STOP)
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_PROGRESSE)
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_JOUE)
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_PAUSE)
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_CHANGE_CHANSON)
        notificateur_evenement.add_event(ListeLectureModele.EVENEMENT_LECTURE_CHARGEMENT)

        liste_lecture_modele = ListeLectureModele(notificateur_evenement)
        lecteur_service = AbstractLecteurService(Mock())

        self.assertEqual(None, liste_lecture_modele.chanson_courante())
        self.assertEqual(None, liste_lecture_modele.jouer_chanson_suivante(lecteur_service))
        self.assertEqual(None, liste_lecture_modele.jouer_chanson_courante(lecteur_service))
        self.assertEqual(None, liste_lecture_modele.rejouer_chanson_courante(lecteur_service))
        self.assertEqual(None, liste_lecture_modele.mettre_en_pause_ou_relancer_chanson(lecteur_service))
        self.assertEqual(EtatLecture.STOP, liste_lecture_modele.etat_lecture)

        liste_lecture_modele.ajouter_chanson(self.chanson_1)
        self.assertEqual(None, liste_lecture_modele.jouer_chanson_suivante(lecteur_service), "Il n'y a pas de chanson suivante à jouer, il n'y a que la chanson courante qui est jouable")
        self.assertEqual(EtatLecture.STOP, liste_lecture_modele.etat_lecture)
        self.assertEqual(self.chanson_1, liste_lecture_modele.jouer_chanson_courante(lecteur_service))
        self.assertEqual(EtatLecture.JOUE, liste_lecture_modele.etat_lecture)
        liste_lecture_modele.mettre_en_pause_ou_relancer_chanson(lecteur_service)
        self.assertEqual(EtatLecture.PAUSE, liste_lecture_modele.etat_lecture)
        liste_lecture_modele.mettre_en_pause_ou_relancer_chanson(lecteur_service)
        self.assertEqual(EtatLecture.JOUE, liste_lecture_modele.etat_lecture)
        liste_lecture_modele.arreter_chanson(lecteur_service)
        self.assertEqual(EtatLecture.STOP, liste_lecture_modele.etat_lecture)
        liste_lecture_modele.arreter_chanson(lecteur_service)
        self.assertEqual(EtatLecture.STOP, liste_lecture_modele.etat_lecture, "Si la lecture est déjà stopée on reste dans cet état")

        self.assertEqual(None, liste_lecture_modele.jouer_chanson_suivante(lecteur_service))
        self.assertEqual(EtatLecture.STOP, liste_lecture_modele.etat_lecture)

        liste_lecture_modele.ajouter_chanson(self.chanson_2)
        liste_lecture_modele.ajouter_chanson(self.chanson_3)
        self.assertEqual(self.chanson_2, liste_lecture_modele.jouer_chanson_suivante(lecteur_service))
        self.assertEqual(EtatLecture.JOUE, liste_lecture_modele.etat_lecture)
        self.assertEqual(self.chanson_3, liste_lecture_modele.jouer_chanson_suivante(lecteur_service))
        self.assertEqual(EtatLecture.JOUE, liste_lecture_modele.etat_lecture)

        self.assertEqual(None, liste_lecture_modele.jouer_chanson_suivante(lecteur_service))

        self.assertEqual(self.chanson_3, liste_lecture_modele.chanson_courante())

        self.assertEqual(self.chanson_2, liste_lecture_modele.jouer_chanson_precedente(lecteur_service))
        self.assertEqual(self.chanson_1, liste_lecture_modele.jouer_chanson_precedente(lecteur_service))
        self.assertEqual(EtatLecture.JOUE, liste_lecture_modele.etat_lecture)
        self.assertEqual(None, liste_lecture_modele.jouer_chanson_precedente(lecteur_service))

        self.assertEqual(self.chanson_1, liste_lecture_modele.chanson_courante())
        self.assertEqual(EtatLecture.JOUE, liste_lecture_modele.etat_lecture)

        self.assertEqual(self.chanson_1_5, liste_lecture_modele.inserer_puis_jouer_chanson(self.chanson_1_5, lecteur_service))
        self.assertEqual(EtatLecture.JOUE, liste_lecture_modele.etat_lecture)
        self.assertEqual(self.chanson_1, liste_lecture_modele.jouer_chanson_precedente(lecteur_service))
        self.assertEqual(self.chanson_1_5, liste_lecture_modele.jouer_chanson_suivante(lecteur_service))
        self.assertEqual(self.chanson_2, liste_lecture_modele.jouer_chanson_suivante(lecteur_service))
        self.assertEqual(EtatLecture.JOUE, liste_lecture_modele.etat_lecture)
