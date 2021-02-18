import socket


def Main():
    port = 8000
    client_binding = ('192.168.56.1', port)

    s = socket.socket()
    s.connect(client_binding)

    filename = input("Please write the name of the file:  ")
    if filename != 'q':
        s.send(filename.encode())
        data = s.recv(1024)
        if data[:6] == b'EXISTS':
            filesize = int(data[6:])
            message = input("This file exists, " + str(filesize) +
                            "Bytes, would you like to download it? (Y/N) ? ")
            if message == 'Y':
                s.send(b'OK')
                f = open('new_' + filename, 'wb')
                data = s.recv(1024)
                TotalRecv = len(data)
                f.write(data)
                while TotalRecv < filesize:
                    data = s.recv(1024)
                    TotalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format(
                        (TotalRecv/float(filesize))*100) + "% Done")
                print("Your Download is complete")
        else:
            print("File does not exists")
    s.close()


if __name__ == '__main__':
    Main()
