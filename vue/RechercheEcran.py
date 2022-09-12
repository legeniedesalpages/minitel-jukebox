__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import inject
from minitel.Minitel import Minitel
from minitel.ui.ChampTexte import ChampTexte
from minitel.ui.Label import Label

from controleur.RechercheControleur import RechercheControleur
from controleur.composant.LecteurComposantControleur import LecteurComposantControleur
from vue.composant.AudioComposant import AudioComposant
from vue.composant.JukeBoxConteneur import JukeBoxConteneur
from vue.composant.LecteurComposant import LecteurComposant
from vue.composant.MenuFixeComposant import MenuFixeComposant


class RechercheEcran:

    @inject.autoparams()
    def __init__(self, minitel: Minitel, audio_composant: AudioComposant, lecteur_composant: LecteurComposant,
                 recherche_controleur: RechercheControleur, lecteur_composant_controleur: LecteurComposantControleur):
        self.__minitel = minitel
        self.__audio_composant = audio_composant
        self.__lecteur_composant = lecteur_composant
        self.__recherche_controleur = recherche_controleur
        self.__lecteur_composant_controleur = lecteur_composant_controleur
        self.__champ_saisie = None

    def afficher(self):
        conteneur = JukeBoxConteneur(self.__minitel, self.appuie_touche_envoi, self.appuie_touche_entree)

        texte_recherche = "Rechercher une chanson par son nom:"
        conteneur.ajoute(Label(self.__minitel, posx=1, posy=1, valeur=texte_recherche, couleur="blanc"))
        conteneur.ajoute(Label(self.__minitel, posx=2, posy=3, valeur="Chanson:", couleur="vert"))
        self.__champ_saisie = ChampTexte(self.__minitel, posx=11, posy=3, longueur_visible=25, longueur_totale=25)
        conteneur.ajoute(self.__champ_saisie)

        conteneur.ajoute(MenuFixeComposant(self.__minitel, posy=21, texte="Lancer recherche", menu="ENTRER"))
        conteneur.ajoute(MenuFixeComposant(self.__minitel, posy=22, texte="Lire la première chanson", menu="ENVOI"))
        conteneur.ajoute(MenuFixeComposant(self.__minitel, posy=23, texte="Précédentes lectures", menu="SOMMAIRE"))

        self.__lecteur_composant.positionnement_curseur(11, 3, self.__champ_saisie)

        conteneur.ajoute(self.__audio_composant)
        conteneur.ajoute(self.__lecteur_composant)

        conteneur.affiche()
        conteneur.executer()

        self.__lecteur_composant.fermer()

    def appuie_touche_envoi(self):
        chanson = self.__champ_saisie.valeur
        self.__lecteur_composant_controleur.action_lire_chanson(chanson)

    def appuie_touche_entree(self):
        print("entree")
