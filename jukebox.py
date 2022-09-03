__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

import inject

from minitel.Minitel import Minitel
from configuration.AudioConfiguration import produire_audio_service
from configuration.MinitelConfiguration import produire_minitel
from service.AudioService import AudioService
from service.JukeBox import JukeBox


def my_config(binder):
    logging.debug("Configuration de l'injecteur de dépendance")
    binder.bind(Minitel, produire_minitel())
    binder.bind(AudioService, produire_audio_service())


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)-5s] %(filename)s:%(lineno)d -> %(message)s"
    )

    inject.configure(my_config)

    logging.info("Lancement du Jukebox Minitel")
    JukeBox().demarrer()
