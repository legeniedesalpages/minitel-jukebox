__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import logging

import inject
from minitel.Minitel import Minitel
from pyobservable import Observable

from modele.lecteur.ListeLectureModele import ListeLectureModele, EtatLecture
from service.minitel.MinitelConstante import CaracteresMinitel
from service.minitel.MinitelExtension import MinitelExtension
from vue.commun.Affichable import Affichable


class BarreLectureVue(Affichable):
    LARGEUR_BARRE = 40

    __notificateur_evenement = inject.attr(Observable)
    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)

    def __init__(self, liste_lecture_modele: ListeLectureModele, callback_positionnement_curseur):
        self._liste_lecture_modele = liste_lecture_modele
        self.__callback_positionnement_curseur = callback_positionnement_curseur

    def afficher(self):
        self.__notificateur_evenement.bind(ListeLectureModele.EVENEMENT_LECTURE_STOP, self._mettre_a_jour_statut)
        self.__notificateur_evenement.bind(ListeLectureModele.EVENEMENT_LECTURE_JOUE, self._mettre_a_jour_statut)
        self.__notificateur_evenement.bind(ListeLectureModele.EVENEMENT_LECTURE_PAUSE, self._mettre_a_jour_statut)
        self.__notificateur_evenement.bind(ListeLectureModele.EVENEMENT_LECTURE_CHARGEMENT, self._mettre_a_jour_statut)
        self.__notificateur_evenement.bind(ListeLectureModele.EVENEMENT_LECTURE_PROGRESSE, self._mettre_a_jour_progression)
        self.__notificateur_evenement.bind(ListeLectureModele.EVENEMENT_LECTURE_CHANGE_CHANSON, self._mettre_a_jour_titre)
        self._mettre_a_jour_statut()
        self._mettre_a_jour_titre()
        self._mettre_a_jour_progression()

    def _mettre_a_jour_statut(self):
        logging.debug("BarreLectureVue: mise a jour statut")
        self.__minitel.position(1, 24)
        self.__minitel.couleur(1)

        self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()
        if self._liste_lecture_modele.etat_lecture == EtatLecture.PAUSE:
            self.__minitel.envoyer(CaracteresMinitel.STATUT_PAUSE.caractere)
        elif self._liste_lecture_modele.etat_lecture == EtatLecture.JOUE:
            self.__minitel.envoyer(CaracteresMinitel.STATUT_LECTURE.caractere)
        elif self._liste_lecture_modele.etat_lecture == EtatLecture.CHARGEMENT:
            self.__minitel.envoyer(CaracteresMinitel.STATUT_CHARGEMENT.caractere)
        else:
            self.__minitel.envoyer(CaracteresMinitel.STATUT_STOP.caractere)
        self.__minitel_extension.revenir_jeu_caractere_standard()

        self.__minitel.effet(inversion=True)
        self.__minitel.envoyer("|")
        self.__minitel.effet(inversion=False)

        self.__callback_positionnement_curseur()

    def _mettre_a_jour_progression(self):
        logging.debug("BarreLectureVue: mise a jour progression")
        self.__minitel.position(self.LARGEUR_BARRE - 3, 24)
        self.__minitel.couleur(1)

        if self._liste_lecture_modele.progression_chanson_courante is None:
            avancement = "|   "
        elif self._liste_lecture_modele.progression_chanson_courante < 10:
            avancement = f"| {self._liste_lecture_modele.progression_chanson_courante}%"
        elif self._liste_lecture_modele.progression_chanson_courante < 100:
            avancement = f"|{self._liste_lecture_modele.progression_chanson_courante}%"
        else:
            avancement = "|fin"

        self.__minitel.effet(inversion=True)
        self.__minitel.envoyer(avancement)
        self.__minitel.effet(inversion=False)

        self.__callback_positionnement_curseur()

    def _mettre_a_jour_titre(self):
        logging.debug("BarreLectureVue: mise a jour titre")
        self.__minitel.position(3, 24)
        self.__minitel.couleur(1)

        if self._liste_lecture_modele.chanson_courante() is None:
            nom_chanson = ''
        else:
            nom_chanson = self._liste_lecture_modele.chanson_courante().titre

        if len(nom_chanson) > self.LARGEUR_BARRE - 5:
            texte = f"{nom_chanson[:self.LARGEUR_BARRE - 5]}"
        else:
            texte = nom_chanson + (' ' * (self.LARGEUR_BARRE - len(nom_chanson) - 5))

        self.__minitel.effet(inversion=True)
        self.__minitel.envoyer(texte)
        self.__minitel.effet(inversion=False)

        self.__callback_positionnement_curseur()

    def fermer(self):
        self.__notificateur_evenement.unbind(ListeLectureModele.EVENEMENT_LECTURE_STOP, self._mettre_a_jour_statut)
        self.__notificateur_evenement.unbind(ListeLectureModele.EVENEMENT_LECTURE_JOUE, self._mettre_a_jour_statut)
        self.__notificateur_evenement.unbind(ListeLectureModele.EVENEMENT_LECTURE_PAUSE, self._mettre_a_jour_statut)
        self.__notificateur_evenement.unbind(ListeLectureModele.EVENEMENT_LECTURE_CHARGEMENT, self._mettre_a_jour_statut)
        self.__notificateur_evenement.unbind(ListeLectureModele.EVENEMENT_LECTURE_PROGRESSE, self._mettre_a_jour_progression)
        self.__notificateur_evenement.unbind(ListeLectureModele.EVENEMENT_LECTURE_CHANGE_CHANSON, self._mettre_a_jour_titre)
