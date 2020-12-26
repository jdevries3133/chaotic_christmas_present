from time import sleep
import signal
import sys
import socket
import subprocess
from pathlib import Path
import logging


from .exceptions import SubprocessServerNotResponding, ImproperlyConfigured

logger = logging.getLogger(__name__)


class SubprocessServer:
    """
    Manage a single server running ./server.Server in a subprocess.
    """
    def __init__(self, host: str, port: int, message: str):
        self.host = host
        self.port = port
        self.message = message
        self.is_healthy = False
        self.server = None


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
        self._check_health()

    def restart(self):
        self.stop()
        self.start()

    def stop(self):
        if not self.server:
            self.is_healthy = False
            return
        self.server.terminate()
        self.server.wait()
        self.is_healthy = False

    def _check_health(self) -> bool:
        """
        Return True when the server responds, or raise an exception
        if there is no response after 5 tries each five seconds apart.
        """
        if self.is_healthy:
            return True
        for _ in range(5):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((self.host, self.port))
                    recieved = b''
                    while data := sock.recv(1024):
                        recieved += data
                    if str(recieved, 'utf-8') == self.message:
                        self.is_healthy = True
                        return True
            except (ConnectionRefusedError, OSError):
                sleep(1)
        raise SubprocessServerNotResponding

class SubprocessServerManager:
    """
    Manage many simple TCP servers (instances of SubprocessServer above).
    Each server will listen on a single port and echo a fixed message to any
    connection.
    """

    def __init__(self, schema: dict):
        self.is_healthy = False  # meaning that servers are up and running
        self.servers = {}

        signal.signal(signal.SIGINT, self.stop)

        self._validate_schema(schema)
        for server_name, server in schema.items():
            self.servers[server_name] = SubprocessServer(
                server['host'],
                server['port'],
                server['message'],
            )

    def start(self):
        print(f'Starting {len(self.servers)} servers.')
        for server_name, server in self.servers.items():
            logger.info(
                f'Started server: {server_name} on port {server.host}:'
                f'{server.port} with message {server.message}'
            )
            server.start()
        self._check_health()
        self._wait()

    def stop(self, *a, **kw):
        print(f'Stopping {len(self.servers)} servers.')
        for server_name, server in self.servers.items():
            logger.info(
                f'Stopped server: {server_name} on port {server.host}:'
                f'{server.port} with message {server.message}'
            )
            server.stop()

    def restart(self):
        self.stop()
        self.start()

    def _wait(self):
        """
        While subprocesses are running, wait for an exit signal.
        """
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            self.stop()
            sys.exit()

    def _check_health(self) -> bool:
        """
        Wait until all subprocesses have started and connections are available
        with a timeout.
        """
        self.is_healthy = True
        for server_name, server in self.servers.items():
            if not server.is_healthy:
                logger.info(
                    'Health state set to false because of the server with a '
                    f'name of {server_name} on {server.host}:{server.port} '
                )
                self.is_healthy = False
        return self.is_healthy

    @ staticmethod
    def _validate_schema(schema):
        """
        Should look like this:
        {
            "server_name": {
                "host": str
                "port": int,
                "message": str,
                "server" SubprocessServer instance
            },
            ...
        }
        """
        used_ports = set()
        for v in schema.values():
            for item, type_ in {
                    'host': str,
                    'port': int,
                    'message': str
            }.items():
                if item not in v:
                    raise ImproperlyConfigured
                if not isinstance(v[item], type_):
                    raise ImproperlyConfigured
            if v['port'] in used_ports:
                raise ImproperlyConfigured(f'Two servers want port {v["port"]}')
            used_ports.add(v['port'])
