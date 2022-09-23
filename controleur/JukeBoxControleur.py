__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject

from service.recherche.GenerateurRecherche import GenerateurRecherche
from modele.JukeBoxModele import JukeBoxModele, TypeRecherche, EvenementSortieEcran
from vue.EcranDemarrageVue import EcranDemarrageVue
from vue.EcranFinVue import EcranFinVue
from vue.EcranVisualisationChanson import EcranVisualisationChanson
from vue.bidule.Sablier import Sablier


class JukeBoxControleur:

    __sablier = inject.attr(Sablier)

    def __init__(self):
        logging.debug("Initialisation du JukeBox")
        self.__generateur_recherche = GenerateurRecherche()

    def demarrer(self):
        logging.info(f"Démarrage du JukeBox")
        EcranDemarrageVue().afficher()

        juke_box_modele = JukeBoxModele(TypeRecherche.YOUTUBE)

        evenement_sortie_ecran = EvenementSortieEcran.AFFICHER_RECHERCHE
        while evenement_sortie_ecran is not EvenementSortieEcran.ARRETER_APPLICATION:

            while evenement_sortie_ecran == EvenementSortieEcran.AFFICHER_RECHERCHE:
                logging.info(f"Afficher la recherche {juke_box_modele.type_recherche}")
                controleur_recherche = self.__generateur_recherche.generer(juke_box_modele)
                evenement_sortie_ecran = controleur_recherche.afficher_ecran_recherche()

            if evenement_sortie_ecran == EvenementSortieEcran.VISUALISER_CHANSON:
                logging.info("Afficher la visualisation")
                ecran_visualisation = EcranVisualisationChanson()
                evenement_sortie_ecran = ecran_visualisation.afficher()

            logging.info(f"Evenement de sortie: {evenement_sortie_ecran}")

        EcranFinVue().afficher()

    def fermer(self):
        self.__sablier.eteindre()
