import socket
from unittest import TestCase

from ..subprocess_server_manager import SubprocessServerManager, SubprocessServer
from ..exceptions import ImproperlyConfigured

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
            'test message',
        )
        self.subprocess_server.start()

    def tearDown(self):
        self.subprocess_server.stop()

    def test_server_responds_immediately_after_start_returns(self):
        msg = str(self.get('127.0.0.1', 6000), 'utf-8')
        self.assertEqual(msg, 'test message')

    def test_server_behaves_same_after_restart(self):
        self.subprocess_server.restart()
        msg = str(self.get('127.0.0.1', 6000), 'utf-8')
        self.assertEqual(msg, 'test message')


class TestSubprocessServerManager(TestCase):
    """
    Integration test of the SubprocessServerManager. Tests that the manager
    class spins up many servers in response to a schema.
    """

    def setUp(self):
        self.manager = SubprocessServerManager({
            'test_server_1': {
                'host': '127.0.0.1',
                'port': 6001,
                'message': 'test server 1 message'
            },
            'test_server_2': {
                'host': '127.0.0.1',
                'port': 6002,
                'message': 'test server 2 message'
            },
            'long_message': {
                'host': '127.0.0.1',
                'port': 6003,
                'message': (
                    'test server 2 messageWe are experiencing strong winds and '
                    'freezing temperatures." Freezing is describing the '
                    'temperature, so it is an adjective.'
                ),
            },
        })

    def tearDown(self):
        self.manager.stop()


    def test_schema_validation(self):
        bad_schemas = [
            {
                # missing port
                'server 1': {
                    'host': '127.0.0.1',
                    'message': 'hi',
                },
                'server 2': {
                    'host': '127.0.0.1',
                    'message': 'hi',
                },
            },
            {
                # missing host
                'server 1': {
                    'port': 5000,
                    'message': 'hi',
                },
                'server 2': {
                    'port': 5000,
                    'message': 'hi',
                },
            },
            {
                # port is str, not int
                'server 1': {
                    'host': '127.0.0.1',
                    'port': '1000',
                    'message': 'hi',
                },
                'server 2': {
                    'host': '127.0.0.1',
                    'port': '1000',
                    'message': 'hi',
                },
            },
        ]
        for schema in bad_schemas:
            with self.assertRaises(ImproperlyConfigured):
                SubprocessServerManager(schema)

    def test_two_servers_cannot_request_same_port(self):
        schema = {
            's1': {
                'host': '127.0.0.1',
                'port': 1000,
                'message': 'hi',
            },
            's2': {
                'host': '127.0.0.1',
                'port': 1000,
                'message': 'hi',
            },
        }
        with self.assertRaises(ImproperlyConfigured):
            SubprocessServerManager(schema)
    def test_starts_and_stops(self):
        self.manager.start()
