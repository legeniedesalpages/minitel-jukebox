__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-06-18"
__version__ = "1.0.0"

from modele.lecteur.BibliothequeSpotify import BibliothequeSpotify


class BibliothequeSpotifyModele:
    liste_bibliotheque: list[BibliothequeSpotify]

    def __init__(self):
        self.liste_bibliotheque = []
