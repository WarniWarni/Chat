import socket
import sys


# TCP/IP Socket
_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

# bind the socket to the port
server_address = ('localhost', 10000)
_socket.bind(server_address)


_socket.listen(1)

while True:
    print('Waiting for a connection')
    connection, client_address = _socket.accept()

    try:
        print("connection from {}".format(client_address))

        # receive data in small chunks and retransmit
        while True:
            data = connection.recv(16)
            print("received: {}".format(data))

            if data:
                print("sending back")
                connection.sendall(data)

            else:
                print("no more data from {}".format(client_address))
                break
    finally:
        # clean up connection
        connection.close()


