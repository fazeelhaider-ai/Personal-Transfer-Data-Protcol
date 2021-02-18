import socket
import threading
import os.path
from os import path


def filesender(name, sock):
    filename = sock.recv(1024)
    if path.exists(filename):
        sock.send(b'EXISTS' + str(os.path.getsize(filename)).encode())
        userResponse = sock.recv(1024)
        if userResponse[:2] == b'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERROR")
    sock.close()


def Main():
    port = 8000

    s = socket.socket()
    server_binding = ('192.168.56.1', port)
    s.bind(server_binding)

    s.listen(5)

    print("Server Started.")
    while True:
        clientsocket, address = s.accept()
        print("client connected ip:" + str(address))
        t = threading.Thread(target=filesender, args=(
            "filesenderThread", clientsocket))
        t.start()
    s.close()


if __name__ == "__main__":
    Main()
