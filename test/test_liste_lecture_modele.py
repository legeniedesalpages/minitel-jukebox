__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import unittest

from modele.Chanson import Chanson
from modele.ListeLectureModele import ListeLectureModele


class ListeLectureModeleTest(unittest.TestCase):

    def test_upper(self):
        liste_lecture_modele = ListeLectureModele()
        liste_lecture_modele.ajouter_chanson(Chanson("1", "un", "01:00", "http://image"))
        # self.assertEqual(liste_lecture_modele., 'FOOd')
