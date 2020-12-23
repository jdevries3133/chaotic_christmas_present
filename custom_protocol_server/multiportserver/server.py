"""
This server and many like it will be run in subprocesses. As such,
this is a standalone module which will be spawned and destroyed by a
parent process at any time.
"""

import argparse
import signal
import logging
import sys
import socket
from time import sleep

logger = logging.getLogger(__name__)


class Server:
    """
    Very simple tcp server that listens to a socket and responds to all
    connections with a plain text message.
    """
    def __init__(self, host: str, port: int, message: bytes):
        self.host = host
        self.port = port
        self.message = message
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # setup graceful exit
        self.is_listening = True
        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)

        # open socket and start listening
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def serve(self):
        """
        Infinite loop until SIGINT or SIGTERM
        """
        while self.is_listening:
            self._send_message()

    def _send_message(self):
        conn, addr = self.socket.accept()
        with conn:
            conn.sendall(self.message)
        return conn, addr

    def exit(self, *a, **kw):
        self.is_listening = False
        self.socket.close()
        sleep(3)  # must account for OS-level TIME_WAIT


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=(
            'Simple TCP Server that will always echo a given message when '
            'connected to through a given port on a given host'
        )
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind to. Default is localhost.'
    )
    parser.add_argument(
        '--port',
        default='6000',
        type=int,
        help='Port to listen on. Default is 6000'
    )
    parser.add_argument(
        '--message',
        default='Hello, world!',
        help=(
            'Message to echo when the port and host are connected to. Default '
            'Hello, world!'
        )
    )
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        print('WARN: Running server with defaults.')
    server = Server(args.host, args.port, bytes(args.message, 'utf-8'))
    server.serve()
