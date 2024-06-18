__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"


class Chanson:
    def __init__(self, identifiant_video, titre, duree, url_image):
        self.identifiant_video = identifiant_video
        self.titre = titre
        self.duree = duree
        self.url_stream = f"https://www.youtube.com/watch?v={identifiant_video}"
        self.url_image = url_image

    def __str__(self) -> str:
        return f"id: {self.identifiant_video}, titre: {self.titre}, duree: {self.duree}, url_stream: {self.url_stream}, image: {self.url_image}"
