__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging
import unittest

from modele.Chanson import Chanson
from modele.ListeLectureModele import ListeLectureModele, ModeRepetition, ModeLecture
from modele.RecuperateurChanson import RecuperateurChanson


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

    def test_doit_recuperer_chanson_lecture_simple_sans_repetition(self):
        recuperateur_chanson = RecuperateurChanson()
        mode_repetition = ModeRepetition.PAS_DE_REPETITION
        mode_lecture = ModeLecture.AVANCE
        liste_lecture_modele = ListeLectureModele(recuperateur_chanson, mode_repetition, mode_lecture)

        self.assertEqual(liste_lecture_modele.chanson_courante(), None)

        liste_lecture_modele.ajouter_chanson(self.chanson_1)
        self.assertEqual(liste_lecture_modele.chanson_suivante(), self.chanson_1)
        self.assertEqual(liste_lecture_modele.chanson_suivante(), None)

        liste_lecture_modele.ajouter_chanson(self.chanson_2)
        liste_lecture_modele.ajouter_chanson(self.chanson_3)
        self.assertEqual(liste_lecture_modele.chanson_suivante(), self.chanson_2)
        self.assertEqual(liste_lecture_modele.chanson_suivante(), self.chanson_3)
        self.assertEqual(liste_lecture_modele.chanson_suivante(), None)

        self.assertEqual(liste_lecture_modele.chanson_courante(), self.chanson_3)

        self.assertEqual(liste_lecture_modele.chanson_precedente(), self.chanson_2)
        self.assertEqual(liste_lecture_modele.chanson_precedente(), self.chanson_1)
        self.assertEqual(liste_lecture_modele.chanson_precedente(), None)

        self.assertEqual(liste_lecture_modele.chanson_courante(), self.chanson_1)

    def test_doit_recuperer_chanson_lecture_simple_avec_repetition_chanson(self):
        recuperateur_chanson = RecuperateurChanson()
        mode_repetition = ModeRepetition.UNE_SEULE_CHANSON
        mode_lecture = ModeLecture.AVANCE
        liste_lecture_modele = ListeLectureModele(recuperateur_chanson, mode_repetition, mode_lecture)

        self.assertEqual(liste_lecture_modele.chanson_courante(), None)

        liste_lecture_modele.ajouter_chanson(self.chanson_1)
        self.assertEqual(liste_lecture_modele.chanson_suivante(), self.chanson_1)
        self.assertEqual(liste_lecture_modele.chanson_suivante(), self.chanson_1)

        liste_lecture_modele.ajouter_chanson(self.chanson_2)
        liste_lecture_modele.ajouter_chanson(self.chanson_3)
        self.assertEqual(liste_lecture_modele.chanson_suivante(), self.chanson_2)
        self.assertEqual(liste_lecture_modele.chanson_suivante(), self.chanson_3)
        self.assertEqual(liste_lecture_modele.chanson_suivante(), None)

        self.assertEqual(liste_lecture_modele.chanson_courante(), self.chanson_3)

        self.assertEqual(liste_lecture_modele.chanson_precedente(), self.chanson_2)
        self.assertEqual(liste_lecture_modele.chanson_precedente(), self.chanson_1)
        self.assertEqual(liste_lecture_modele.chanson_precedente(), None)

        self.assertEqual(liste_lecture_modele.chanson_courante(), self.chanson_1)


