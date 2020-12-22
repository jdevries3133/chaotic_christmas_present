"""
This server and many like it will be run in subprocesses. As such,
this is a standalone module which will be spawned and destroyed by a
parent process at any time.
"""

import argparse
import os
import logging
import sys
import socket

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

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    conn.sendall(self.message)
                self._housekeep(conn, addr)

    def _housekeep(self, last_conn, last_addr):
        """
        Any side effects inbetween connections can happen here. For example
        sending data through a pipe to the parent or reading from a database
        to update the message.
        """


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
            '"Hello, world!"'
        )
    )
    args = parser.parse_args()
    if len(sys.argv) == 1:
        print('WARN: Running server with defaults.')
        parser.print_help()
    server = Server(args.host, args.port, bytes(args.message, 'utf-8'))
    server.listen()
