__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-05-31"
__version__ = "1.0.0"


class Wifi:
    FORCE_MAX = 3

    force: int
    nom: str

    def __init__(self, nom: str, force: int):
        self.nom = nom
        self.force = force

    def __str__(self):
        return f"{self.nom}, force {self.force}/{self.FORCE_MAX}"
