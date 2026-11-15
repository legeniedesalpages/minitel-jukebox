import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock, patch

from minitel.Sequence import Sequence
from minitel.constantes import SOMMAIRE, SUITE
from controleur.bluetooth.BluetoothControleur import BluetoothControleur
from controleur.commun.JukeBoxControleur import JukeBoxControleur
from modele.lecteur.JukeBoxModele import JukeBoxModele, Ecran

from service.ErreurService import ErreurService
from service.lecteur.VlcService import VlcService
from vue.commun.AbstractEcran import AbstractEcran


class ErreursInterfaceTest(unittest.TestCase):
    def setUp(self):
        while ErreurService.recuperer() is not None:
            pass

    def tearDown(self):
        while ErreurService.recuperer() is not None:
            pass

    def tester_ecran(self, erreur_initiale=False, erreur_action=False, erreur_fond=False):
        ecran = AbstractEcran.__new__(AbstractEcran)
        ecran._get_titre_ecran = Mock(return_value="Recherche")
        ecran._get_callback_curseur = Mock()
        ecran._affichage_initial = Mock()
        ecran._gere_touche = Mock()
        ecran.fermer = Mock()
        for attribut in ("bluetooth_modele", "wifi_modele", "liste_lecture_modele", "barre_audio_vue"):
            setattr(ecran, "_AbstractEcran__" + attribut, Mock())
        navigation = Mock()
        navigation.gere_touche.return_value = True
        ecran._controleur = Mock()
        ecran._controleur._controleur_pouvant_gerer_touche = [navigation]
        ecran._controleur.gere_touche.return_value = True
        minitel = Mock()
        extension = Mock()
        if erreur_initiale:
            ecran._affichage_initial.side_effect = RuntimeError("Echec ouverture")
        if erreur_action:
            ecran._gere_touche.side_effect = RuntimeError("Echec recherche")
            minitel.recevoir_sequence.side_effect = [Sequence("x"), Sequence(SOMMAIRE)]
        else:
            minitel.recevoir_sequence.return_value = Sequence(SOMMAIRE)
        if erreur_fond:
            ErreurService.signaler("Lecture audio", RuntimeError("Echec VLC"))

        with patch.object(AbstractEcran, "_minitel", minitel), \
                patch.object(AbstractEcran, "_minitel_extension", extension), \
                patch.object(AbstractEcran, "_sablier", Mock()), \
                patch("vue.commun.AbstractEcran.BarreTitreVue"), \
                patch("vue.commun.AbstractEcran.BarreLectureVue"):
            ecran.afficher()

        ecran.fermer.assert_called_once()
        if erreur_initiale or erreur_action or erreur_fond:
            messages = [appel.kwargs.get("texte", "") for appel in extension.envoyer_ligne.call_args_list]
            self.assertIn("Erreur - action interrompue", messages)
            self.assertIn("SOMMAIRE: passer a un autre ecran", messages)
            navigation.gere_touche.assert_called()
        else:
            ecran._controleur.gere_touche.assert_called_once()

    def test_navigation_normale_preservee(self):
        self.tester_ecran()

    def test_suite_bluetooth_ouvre_la_recherche(self):
        modele = JukeBoxModele()
        controleur = BluetoothControleur({}, {"jukebox": modele, "bluetooth": Mock()})
        self.assertEqual(Ecran.ECRAN_BLUETOOTH, modele.ecran_courant)
        self.assertIsNone(modele.ecran_demande)

        self.assertTrue(controleur.gere_touche(Sequence(SUITE)))
        self.assertEqual(Ecran.ECRAN_RECHERCHE, modele.ecran_demande)

    def test_erreur_ouverture_ne_bloque_pas_sommaire(self):
        self.tester_ecran(erreur_initiale=True)

    def test_erreur_action_ne_bloque_pas_sommaire(self):
        self.tester_ecran(erreur_action=True)

    def test_erreur_fond_affichee_sans_action_utilisateur(self):
        self.tester_ecran(erreur_fond=True)

    def test_erreur_callback_vlc_signalee(self):
        controleur = Mock()
        controleur.evenement_fin_chanson.side_effect = RuntimeError("Spotify indisponible")
        service = VlcService(controleur)
        service._evenement_fin_chanson(None)
        self.assertIn("Spotify indisponible", ErreurService.recuperer())

    def test_mode_non_charge_affiche_erreur_et_permet_sommaire(self):
        jukebox = JukeBoxControleur.__new__(JukeBoxControleur)
        modele = JukeBoxModele()
        modele.ecran_courant = Ecran.ECRAN_BIBLIOTHEQUE_SPOTIFY
        jukebox._JukeBoxControleur__jukebox_modele = modele
        minitel = Mock()
        minitel.recevoir_sequence.return_value = Sequence(SOMMAIRE)
        extension = Mock()
        ErreurService.signaler("Chargement Spotify", RuntimeError("Erreur de chargement"))
        with patch("controleur.commun.JukeBoxControleur.inject.instance",
                   side_effect=[minitel, extension]):
            jukebox._JukeBoxControleur__ecran_erreur()
        self.assertEqual(Ecran.ECRAN_VISUALISATION, modele.ecran_demande)
        extension.envoyer_ligne.assert_called()

    def test_file_erreurs_bornee_et_thread_safe(self):
        with patch("service.ErreurService.logging.error"), ThreadPoolExecutor(max_workers=8) as travailleurs:
            list(travailleurs.map(
                lambda numero: ErreurService.signaler("Test", RuntimeError(str(numero))), range(100)))
        messages = []
        while True:
            message = ErreurService.recuperer()
            if message is None:
                break
            messages.append(message)
        self.assertEqual(20, len(messages))
        self.assertEqual(20, len(set(messages)))

    def test_cause_http_et_timeout_explicites(self):
        import requests
        reponse = Mock(status_code=403)
        ErreurService.signaler("Spotify", requests.HTTPError(response=reponse))
        self.assertIn("acces refuse", ErreurService.recuperer())
        ErreurService.signaler("YouTube", requests.Timeout())
        self.assertIn("YouTube. Le service ne repond pas", ErreurService.recuperer())
