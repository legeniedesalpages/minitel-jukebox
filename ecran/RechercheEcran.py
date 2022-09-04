__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

from minitel.Minitel import Minitel
from minitel.ui.ChampTexte import ChampTexte
from minitel.ui.Label import Label

from controleur import JukeBoxControleur
from widget.AudioWidget import AudioWidget
from widget.JukeBoxConteneur import JukeBoxConteneur


class RechercheEcran:

    def __init__(self, minitel: Minitel, juke_box_controleur: JukeBoxControleur):
        self.__minitel = minitel
        self.__juke_box_controleur = juke_box_controleur

    def afficher(self):
        conteneur = JukeBoxConteneur(self.__minitel)

        texte_recherche = "Rechercher une chanson par son nom:"
        conteneur.ajoute(Label(self.__minitel, posx=1, posy=1, valeur=texte_recherche, couleur="blanc"))
        conteneur.ajoute(Label(self.__minitel, posx=2, posy=3, valeur="Chanson:", couleur="vert"))
        conteneur.ajoute(ChampTexte(self.__minitel, posx=11, posy=3, longueur_visible=25, longueur_totale=25))

        conteneur.ajoute(Label(self.__minitel, posx=15, posy=22, valeur="lancer recherche →"))
        conteneur.ajoute(Label(self.__minitel, posx=34, posy=22, valeur="ENTRER"))
        conteneur.ajoute(Label(self.__minitel, posx=8, posy=21, valeur="lire la premiere chanson →"))
        conteneur.ajoute(Label(self.__minitel, posx=35, posy=21, valeur="ENVOI"))
        conteneur.ajoute(Label(self.__minitel, posx=9, posy=23, valeur="precedentes lectures →"))
        conteneur.ajoute(Label(self.__minitel, posx=32, posy=23, valeur="SOMMAIRE"))

        conteneur.ajoute(AudioWidget(self.__minitel, self.__juke_box_controleur))

        conteneur.affiche()
        conteneur.executer()
