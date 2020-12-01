import socket

from server import HOST, PORT, DATA

def test_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        recieved = b''
        while data := s.recv(1024):
            recieved += data
        assert recieved == DATA
