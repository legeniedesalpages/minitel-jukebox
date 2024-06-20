__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-06-18"
__version__ = "1.0.0"


class BibliothequeSpotify:
    identifiant: str
    nom_bibliotheque: str
    nombre_titre_dedans: int

    def __init__(self, identifiant: str, nom_bibliotheque: str, nombre_titre_dedans: int):
        self.identifiant = identifiant
        self.nom_bibliotheque = nom_bibliotheque
        self.nombre_titre_dedans = nombre_titre_dedans

    def __str__(self):
        return f"{self.nom_bibliotheque}({self.nombre_titre_dedans})"
