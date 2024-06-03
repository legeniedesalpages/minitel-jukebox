__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-30"
__version__ = "1.0.0"

import inject
from minitel.Minitel import Minitel
from pyobservable import Observable

from modele.ListeLectureModele import ListeLectureModele, EtatLecture
from service.minitel.MinitelExtension import MinitelExtension
from vue.Affichable import Affichable
from vue.bidule.Sablier import Sablier


class BarreLectureVue(Affichable):
    LARGEUR_BARRE = 40

    __notificateur_evenement = inject.attr(Observable)
    __sablier = inject.attr(Sablier)
    __minitel = inject.attr(Minitel)
    __minitel_extension = inject.attr(MinitelExtension)

    def __init__(self, liste_lecture_modele: ListeLectureModele, callback_positionnement_curseur):
        self._liste_lecture_modele = liste_lecture_modele
        self.__callback_positionnement_curseur = callback_positionnement_curseur

    def afficher(self):
        self.__notificateur_evenement.bind(ListeLectureModele.EVENEMENT_LECTURE_STOP, self._mettre_a_jour_stop)
        self.__notificateur_evenement.bind(ListeLectureModele.EVENEMENT_LECTURE_JOUE, self._mettre_a_jour)
        self.__notificateur_evenement.bind(ListeLectureModele.EVENEMENT_LECTURE_PAUSE, self._mettre_a_jour)
        self.__notificateur_evenement.bind(ListeLectureModele.EVENEMENT_LECTURE_PROGRESSE, self._mettre_a_jour_progression)
        self.__notificateur_evenement.bind(ListeLectureModele.EVENEMENT_LECTURE_CHANGE_CHANSON, self._mettre_a_jour_progression)
        self._mettre_a_jour()

    def _mettre_a_jour_stop(self):
        self._mettre_a_jour()

    def _mettre_a_jour_progression(self):
        self._mettre_a_jour()

    def _mettre_a_jour(self):
        if self._liste_lecture_modele.progression_chanson_courante is not None:
            pourcent = f"|{self._liste_lecture_modele.progression_chanson_courante}%"
        else:
            pourcent = ''

        if self._liste_lecture_modele.chanson_courante() is None:
            nom_chanson = ' '
        else:
            nom_chanson = self._liste_lecture_modele.chanson_courante().titre

        longeur = self.LARGEUR_BARRE - (1 + len(nom_chanson) + len(pourcent))
        if longeur < 0:
            texte = f"{nom_chanson[:self.LARGEUR_BARRE - 1 - len(pourcent)]}{pourcent}"
        else:
            texte = nom_chanson + (' ' * longeur) + pourcent

        self.__minitel.position(1, 24)
        self.__minitel.couleur(1)

        self.__minitel_extension.demarrer_affichage_jeu_caractere_redefinit()
        if self._liste_lecture_modele.etat_lecture == EtatLecture.PAUSE:
            self.__minitel.envoyer("P")
        elif self._liste_lecture_modele.etat_lecture == EtatLecture.JOUE:
            self.__minitel.envoyer("L")
        else:
            self.__minitel.envoyer("S")
        self.__minitel_extension.revenir_jeu_caractere_standard()

        self.__minitel.effet(inversion=True)
        self.__minitel.envoyer(texte)
        self.__minitel.effet(inversion=False)

        self.__callback_positionnement_curseur()

    def fermer(self):
        self.__notificateur_evenement.unbind(ListeLectureModele.EVENEMENT_LECTURE_STOP, self._mettre_a_jour_stop)
        self.__notificateur_evenement.unbind(ListeLectureModele.EVENEMENT_LECTURE_JOUE, self._mettre_a_jour)
        self.__notificateur_evenement.unbind(ListeLectureModele.EVENEMENT_LECTURE_PAUSE, self._mettre_a_jour)
        self.__notificateur_evenement.unbind(ListeLectureModele.EVENEMENT_LECTURE_PROGRESSE, self._mettre_a_jour_progression)
        self.__notificateur_evenement.unbind(ListeLectureModele.EVENEMENT_LECTURE_CHANGE_CHANSON, self._mettre_a_jour_progression)
