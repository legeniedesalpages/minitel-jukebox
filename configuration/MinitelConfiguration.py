__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from minitel.Minitel import Minitel


def produire_minitel() -> Minitel:
    minitel = Minitel("/dev/ttyUSB0")
    minitel.deviner_vitesse()
    minitel.identifier()
    minitel.definir_vitesse(9600)
    minitel.definir_mode("VIDEOTEX")
    minitel.configurer_clavier(etendu=True, curseur=False, minuscule=True)
    minitel.echo(False)
    minitel.curseur(False)
    logging.info(f"Création du minitel, vitesse => {minitel.vitesse}")
    return minitel
