import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000        # Port to listen on (non-privileged ports are > 1023)

DATA = (
   b'00000000011100000000001110000000000000111111111111111111111110000000000000000000'
   b'00000000011100000000001110000000000000000000000110000000000000000000000000000000'
   b'00000000011100000000001110000000000000000000000110000000000000000000000000000000'
   b'00000000011100000000001110000000000000000000000110000000000000000000000000000000'
   b'00000000011100000000001110000000000000000000000110000000000000000000000000000000'
   b'00000000011100000000001110000000000000000000000110000000000000000000000000000000'
   b'00000000011111111111111110000000000000000000000110000000000000000000000000000000'
   b'00000000011111111111111110000000000000000000000110000000000000000000000000000000'
   b'00000000011100000000001110000000000000000000000110000000000000000000000000000000'
   b'00000000011100000000001110000000000000000000000110000000000000000000000000000000'
   b'00000000011100000000001110000000000000000000000110000000000000000000000000000000'
   b'00000000011100000000001110000000000000000000000000000000000000000000000000000000'
   b'00000000011100000000001110000000000000111111111111111111111110000000000000000000'
)

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by ', addr)
                conn.sendall(DATA)
