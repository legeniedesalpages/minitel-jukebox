__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2022-08-28"
__version__ = "1.0.0"

import logging

from minitel.Minitel import Minitel
from minitel.constantes import PRO1, RESET

from service.minitel.MinitelConstante import CaracteresMinitel
from service.minitel.MinitelExtension import MinitelExtension


def produire_minitel() -> Minitel:
    minitel = Minitel("/dev/ttyUSB0")
    minitel.deviner_vitesse()
    minitel.definir_mode("VIDEOTEX")

    for car in CaracteresMinitel:
        minitel.redefinir(car.caractere, car.dessin)

    minitel.appeler([PRO1, RESET], 1)
    minitel.configurer_clavier(etendu=True, curseur=False, minuscule=True)
    minitel.echo(False)
    minitel.curseur(False)

    logging.info(f"Création du minitel terminé, vitesse => {minitel.vitesse}")
    minitel.efface('vraimenttout')
    minitel.recevoir_sequence(bloque=True, attente=None)

    return minitel


def produire_minitel_extension(minitel: Minitel) -> MinitelExtension:
    minitel_extension = MinitelExtension(minitel)
    minitel_extension.revenir_jeu_caractere_standard()
    return minitel_extension
