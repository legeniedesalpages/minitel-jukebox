__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"


class JukeBoxModele:

    def __init__(self):
        self.__est_termine = False

    def arreter_jukebox(self):
        self.__est_termine = True

    def est_termine(self) -> bool:
        return self.__est_termine
