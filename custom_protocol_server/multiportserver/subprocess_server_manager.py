from time import sleep
import socket
import subprocess
from pathlib import Path
import logging


from .exceptions import SubprocessServerNotResponding

logger = logging.getLogger(__name__)


class SubprocessServer:
    """
    Manage a single server running ./server.Server in a subprocess.
    """
    def __init__(self, host: str, port: int, message: bytes):
        self.host = host
        self.port = port
        self.message = message
        self.is_healthy = False

    def start(self):
        self.server = subprocess.Popen(
            [
                'python3.8',
                Path(Path(__file__).parent, 'server.py').resolve(),
                '--host',       self.host,
                '--port',       str(self.port),
                '--message',    self.message,
            ],
        )
        self.check_health()

    def check_health(self):
        """
        Do not return until the server responds, or raise an exception
        after 5 seconds.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            for _ in range(5):
                try:
                    s.connect((self.host, self.port))
                    recieved = b''
                    while data := s.recv(1024):
                        recieved += data
                    return recieved
                except ConnectionRefusedError:
                    sleep(1)

    def stop(self):
        self.server.terminate()
        self.server.wait()


class SubprocessServerManager:
    """
    Manage many simple TCP servers in subprocesses using instances of
    ./server.Server. Each server will listen on a single port and echo
    a fixed message to any connection. Each server will, on its own or in
    chorus with its peers, be cookie crumbs in the greater scavenger hunt.
    """

    def __init__(self, schema: dict):
        self.schema = schema
        self.is_healthy = False  # set to True by health_check when all servers are responding.

    def health_check(self) -> bool:
        """
        Wait until all subprocesses have started and connections are available
        with a timeout.
        """

