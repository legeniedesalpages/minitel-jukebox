import unittest
from unittest.mock import Mock, patch

import requests

from modele.lecteur.BibliothequeSpotifyModele import BibliothequeSpotifyModele
from service.lecteur.SpotifyService import SpotifyAPIError, SpotifyService
from controleur.recherche.BibliothequeSpotifyControleur import BibliothequeSpotifyControleur


class SpotifyServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = SpotifyService.__new__(SpotifyService)
        self.service._SpotifyService__USER_ID = "test-user"
        self.service._SpotifyService__erreur_initialisation = None

    @patch("service.lecteur.SpotifyService.requests.post")
    def test_authentication_error_is_kept_for_the_spotify_screen(self, request_post):
        response = Mock(status_code=401, text="Unauthorized")
        response.raise_for_status.side_effect = requests.HTTPError(
            "401 Unauthorized", response=response)
        request_post.return_value = response

        service = SpotifyService("client", "secret", "user")

        self.assertIn("HTTP 401", service._SpotifyService__erreur_initialisation)
        with self.assertRaisesRegex(SpotifyAPIError, "HTTP 401"):
            service.liste_bibliotheque()

    @patch("service.lecteur.SpotifyService.SpotifyService._SpotifyService__appel_spotify")
    def test_http_error_is_converted_to_a_clear_spotify_error(self, appel_spotify):
        response = Mock(status_code=403, text="Forbidden")
        response.raise_for_status.side_effect = requests.HTTPError(
            "403 Forbidden", response=response)
        appel_spotify.return_value = response

        with self.assertRaisesRegex(SpotifyAPIError, "HTTP 403"):
            self.service.liste_bibliotheque()

    @patch("service.lecteur.SpotifyService.SpotifyService._SpotifyService__appel_spotify")
    def test_invalid_json_is_reported_as_a_spotify_error(self, appel_spotify):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.side_effect = ValueError("invalid JSON")
        appel_spotify.return_value = response

        with self.assertRaisesRegex(SpotifyAPIError, "reponse invalide"):
            self.service.liste_bibliotheque()


class SpotifyLibraryControllerTest(unittest.TestCase):

    def test_displays_screen_when_spotify_library_request_fails(self):
        controller = BibliothequeSpotifyControleur.__new__(BibliothequeSpotifyControleur)
        model = BibliothequeSpotifyModele()
        controller._BibliothequeSpotifyControleur__bibliotheque_spotify_modele = model
        controller._BibliothequeSpotifyControleur__spotify_service = Mock()
        controller._BibliothequeSpotifyControleur__spotify_service.liste_bibliotheque.side_effect = (
            SpotifyAPIError("Acces a la bibliotheque Spotify refuse (HTTP 403)."))
        controller._vue = Mock()

        controller.lancer()

        self.assertEqual([], model.liste_bibliotheque)
        self.assertIn("HTTP 403", model.erreur)
        controller._vue.afficher.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
