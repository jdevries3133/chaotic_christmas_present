import socket
from unittest import TestCase

from ..subprocess_server_manager import SubprocessServerManager, SubprocessServer

class BaseSocketTestCase(TestCase):
    @ staticmethod
    def get(host: str, port: int) -> bytes:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            recieved = b''
            while data := s.recv(1024):
                recieved += data
            return recieved


class TestSubprocessServer(BaseSocketTestCase):

    def setUp(self):
        self.subprocess_server = SubprocessServer(
            '127.0.0.1',
            6000,
            b'test message',
        )
        self.subprocess_server.start()

    def tearDown(self):
        self.subprocess_server.stop()

    def test_server_responds_immediately_after_start_returns(self):
        msg = str(self.get('127.0.0.1', 6000))
        self.assertEqual(msg, b'test message')

class TestSubprocessServerManager(TestCase):
    """
    Integration test of the SubprocessServerManager. Tests that the manager
    class spins up many servers in response to a schema.
    """
