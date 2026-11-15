import unittest
from unittest.mock import Mock, patch

from service.bluetooth.BluetoothService import BluetoothService


class BluetoothServiceTest(unittest.TestCase):

    @patch("service.bluetooth.BluetoothService.subprocess.run")
    def test_retourne_echec_si_la_connexion_bluetooth_echoue(self, executer):
        executer.side_effect = [
            Mock(returncode=0, stdout="Paired: yes\nTrusted: yes\nConnected: no\n"),
            Mock(returncode=0, stdout="Attempting to connect\nFailed to connect: org.bluez.Error.Failed\n")
        ]

        self.assertFalse(BluetoothService.associer_peripherique("08:DF:1F:1C:1C:ED"))
        self.assertEqual(executer.call_count, 2)
        self.assertEqual(executer.call_args_list[1].args[0][1], "connect")

    @patch("service.bluetooth.BluetoothService.subprocess.run")
    def test_ne_relance_pas_une_connexion_deja_active(self, executer):
        executer.return_value = Mock(returncode=0, stdout="Connected: yes\n")

        self.assertTrue(BluetoothService.associer_peripherique("08:DF:1F:1C:1C:ED"))
        self.assertEqual(executer.call_count, 1)

    @patch("service.bluetooth.BluetoothService.subprocess.run")
    def test_appaire_autorise_et_connecte_un_nouveau_peripherique(self, executer):
        executer.side_effect = [
            Mock(returncode=0, stdout="Paired: no\nTrusted: no\nConnected: no\n"),
            Mock(returncode=0, stdout="Pairing successful\n"),
            Mock(returncode=0, stdout="trust succeeded\n"),
            Mock(returncode=0, stdout="Connection successful\n")
        ]

        self.assertTrue(BluetoothService.associer_peripherique("08:DF:1F:1C:1C:ED"))
        self.assertEqual(executer.call_count, 4)


if __name__ == "__main__":
    unittest.main()
