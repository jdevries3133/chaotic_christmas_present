# Try Out Our Tech (Garbage)

Our GarbageTech is on display today! Simply run this python snippet to
get a snappy response from our first TCP protocol, the `helloworldprotocol`!

Do you ever forget how to spell "Hello, World!"? Well, fear not. We've got you!

    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('thomasdevri_es', 1050))
        recieved = b''
        while data := s.recv(1024):
            recieved += data
        print(recieved)
