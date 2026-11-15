import logging
from collections import deque
from threading import Lock
from typing import Optional

import requests


class ErreurService:
    _erreurs = deque(maxlen=20)
    _verrou = Lock()

    @classmethod
    def signaler(cls, contexte: str, erreur: Exception):
        logging.error("%s: %s", contexte, erreur, exc_info=(type(erreur), erreur, erreur.__traceback__))
        if isinstance(erreur, requests.HTTPError) and erreur.response is not None:
            detail = f"Service distant: acces refuse ou indisponible (HTTP {erreur.response.status_code})."
        elif isinstance(erreur, requests.Timeout):
            detail = "Le service ne repond pas dans le delai prevu."
        elif isinstance(erreur, requests.ConnectionError):
            detail = "Connexion reseau impossible. Verifiez Internet."
        elif isinstance(erreur, requests.exceptions.JSONDecodeError):
            detail = "Le service a renvoye une reponse illisible (JSON invalide)."
        elif isinstance(erreur, OSError):
            detail = f"Erreur materielle ou systeme: {erreur}"
        else:
            detail = f"{type(erreur).__name__}: {erreur}"
        message = f"{contexte}. {detail}"
        with cls._verrou:
            if not cls._erreurs or cls._erreurs[-1] != message:
                cls._erreurs.append(message)
        return message

    @classmethod
    def recuperer(cls) -> Optional[str]:
        with cls._verrou:
            return cls._erreurs.popleft() if cls._erreurs else None
