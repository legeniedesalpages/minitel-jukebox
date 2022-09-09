__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject
from minitel.Minitel import Minitel
from minitel.ui.UI import UI
from pyobservable import Observable

from controleur.composant.LecteurComposantControleur import LecteurComposantControleur
from modele.composant.LecteurModele import LecteurModele, EvenementLecteurModele


class LecteurComposant(UI):
    __TOUCHE_ENVOI = [19, 65]
    __TOUCHE_RETOUR = [19, 66]
    __TOUCHE_SUITE = [19, 72]
    __TOUCHE_REPETITION = [19, 67]
    __TOUCHE_ANNULATION = [19, 69]

    __LIGNE_POSITIONNEMENT_BANDEAU = 24

    @inject.autoparams()
    def __init__(self, minitel: Minitel, lecteur_modele: LecteurModele,
                 composant_controleur: LecteurComposantControleur,
                 notificateur_evenement: Observable):
        super().__init__(minitel, 1, 1, 1, 1, "noir")
        self.__minitel = minitel
        self.__lecteur_modele = lecteur_modele
        self.__composant_controleur = composant_controleur
        self.__notificateur_evenement = notificateur_evenement
        self.__avancement_courant = 0
        self.__posx = None
        self.__posy = None
        self.__champ_saisie = None

    def affiche(self):
        self.__enregistrer_evenement()

    def fermer(self):
        self.__oublier_evenement()

    def arret_chanson(self, texte):
        self.__dessine("Lecteur arrété", "", "noir")

    def chargement_chanson(self, texte):
        self.__dessine("Chargement:", texte, "noir")

    def pause_chanson(self, texte):
        self.__dessine("Pause:", texte, "magenta")

    def lecture_chanson(self, texte):
        self.__dessine("Lecture[00:00]:", texte, "noir")

    def avancement_chanson(self, avancement):
        if self.__avancement_courant != avancement:
            self.__avancement_courant = avancement
            minutes, secondes = divmod(avancement, 60)
            texte_avancement = str(minutes).rjust(2, "0") + ":" + str(secondes).rjust(2, "0")
            self.__dessine(f"Lecture[{texte_avancement}]:", self.__lecteur_modele.chanson_courante.titre, "noir")

    def __dessine(self, action, texte, couleur):
        self.__minitel.curseur(False)

        self.__minitel.position(1, LecteurComposant.__LIGNE_POSITIONNEMENT_BANDEAU)
        self.__minitel.couleur("rouge", "blanc")
        self.__minitel.effet(inversion=True)
        self.__minitel.envoyer(" " + action)

        taille_actuelle = 1 + len(action)
        for mot in texte[:39 - taille_actuelle].split(" "):
            self.__minitel.couleur("rouge", couleur)
            self.__minitel.effet(inversion=True)
            self.__minitel.envoyer(" " + mot)
            taille_actuelle += 1 + len(mot)

        if taille_actuelle < 40:
            self.__minitel.envoyer(" ".ljust(40 - taille_actuelle, " "))

        self.__minitel.position(self.__posx + self.__champ_saisie.curseur_x, self.__posy)
        self.__minitel.curseur(True)

    def positionnement_curseur(self, posx, posy, champ_saisie):
        self.__posx = posx
        self.__posy = posy
        self.__champ_saisie = champ_saisie

    def gere_touche(self, sequence):
        touche = sequence.valeurs
        logging.debug(f"Touche appuyée: {touche}")

        if touche == LecteurComposant.__TOUCHE_REPETITION:
            self.__composant_controleur.action_repeter_chanson()
            return True

        if touche == LecteurComposant.__TOUCHE_ANNULATION:
            self.__composant_controleur.action_pause_ou_reprendre()
            return True

        if touche == LecteurComposant.__TOUCHE_ENVOI:
            self.__composant_controleur.action_lire_chanson()
            return True

        if touche == LecteurComposant.__TOUCHE_SUITE:
            self.__composant_controleur.action_chanson_suivante()
            return True

    def __enregistrer_evenement(self):
        self.__notificateur_evenement.bind(EvenementLecteurModele.EVENEMENT_AVANCEMENT_LECTURE, self.avancement_chanson)
        self.__notificateur_evenement.bind(EvenementLecteurModele.EVENEMENT_CHARGEMENT_CHANSON, self.chargement_chanson)
        self.__notificateur_evenement.bind(EvenementLecteurModele.EVENEMENT_PAUSE, self.pause_chanson)
        self.__notificateur_evenement.bind(EvenementLecteurModele.EVENEMENT_LECTURE, self.lecture_chanson)
        self.__notificateur_evenement.bind(EvenementLecteurModele.EVENEMENT_ARRET, self.arret_chanson)
        self.__notificateur_evenement.bind(EvenementLecteurModele.EVENEMENT_FIN_CHANSON, self.arret_chanson)

    def __oublier_evenement(self):
        self.__notificateur_evenement.unbind(EvenementLecteurModele.EVENEMENT_CHARGEMENT_CHANSON,
                                             self.chargement_chanson)
        self.__notificateur_evenement.unbind(EvenementLecteurModele.EVENEMENT_PAUSE, self.pause_chanson)
        self.__notificateur_evenement.unbind(EvenementLecteurModele.EVENEMENT_LECTURE, self.lecture_chanson)
        self.__notificateur_evenement.unbind(EvenementLecteurModele.EVENEMENT_ARRET, self.arret_chanson)
        self.__notificateur_evenement.unbind(EvenementLecteurModele.EVENEMENT_AVANCEMENT_LECTURE,
                                             self.avancement_chanson)
        self.__notificateur_evenement.unbind(EvenementLecteurModele.EVENEMENT_FIN_CHANSON, self.arret_chanson)
