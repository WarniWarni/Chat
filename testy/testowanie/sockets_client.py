import socket
import sys


_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
_socket.connect(server_address)



try:
    # send data
    message = "This is the message. Repeating..."
    print("sending the message")
    _socket.sendall(message)

    # look for response
    amount_received = 0
    amount_expected = len(message)

    while amount_received<amount_expected:
        data = _socket.recv(16)
        amount_received+=len(data)
        print("received data chunk and it is: >>> {} <<<. Amount received = {}".format(data, amount_received))

finally:
    print("closing socket")
    _socket.close()