from pathlib import Path
from io import StringIO
from time import sleep
import socket
import subprocess
import string
from unittest import TestCase

from ..server import Server


class TestServerMessages(TestCase):
    """
    Test that the server behaves consistently for a wide range of messages.
    """
    MESSAGES = [
        b'test message',
        bytes(string.printable, 'utf-8'),
        bytes('😳', 'utf-8'),
    ]

    def setUp(self):
        self.servers = [
            Server(
                '127.0.0.1',
                i + 6000,
                message
            ) for i, message in enumerate(self.MESSAGES)
        ]

    def tearDown(self):
        for server in self.servers:
            server.exit()

    def test_server_sends_messages(self):
        for server in self.servers:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server.host, server.port))
                server._send_message()
                recieved = b''
                while data := s.recv(1024):
                    recieved += data
                self.assertEqual(recieved, server.message)



class TestServerIntegration(TestCase):
    """
    Integration test that runs server in a subprocess.
    """

    HOST = '127.0.0.1'
    PORT = 6000
    MESSAGE = 'test message'
    STDOUT = StringIO()
    STDERR = StringIO()
    def setUp(self):
        self.server_proc = subprocess.Popen(
            [
                'python3.8',
                Path(Path(__file__).parents[1], 'server.py').resolve(),
                '--host',       self.HOST,
                '--port',       str(self.PORT),
                '--message',    self.MESSAGE,
            ],
        )
        sleep(0.2)  # wait for process to start up. This may produce inconsistent behavior

    def tearDown(self):
        # close server
        self.server_proc.terminate()
        self.server_proc.wait()

    def test_server_sends_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            recieved = b''
            while data := s.recv(1024):
                recieved += data
            self.assertEqual(recieved, bytes(self.MESSAGE, 'utf-8'))

    def test_server_sends_message_repeatedly(self):
        for _ in range(5):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.HOST, self.PORT))
                recieved = b''
                while data := s.recv(1024):
                    recieved += data
                self.assertEqual(recieved, bytes(self.MESSAGE, 'utf-8'))
