import socket
import threading
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description='loading ip address')
    parser.add_argument('-ip', '--ip_addr', type=str, help='ip address of the host', required=False)
    args = parser.parse_args()
    IP_ADDR = args.ip_addr
    return IP_ADDR


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1)

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            if data:
                for connection in self.connections:
                    # roześlij info do każdego klienta
                    connection.send(data)
                print(data)
            else:
                break

    def run(self):
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print("{}: {} connected".format(str(a[0]), str(a[1])))


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""), 'windows-1250'))

    def __init__(self, address):
        try:
            self.sock.connect((address, 10000))
            iThread = threading.Thread(target=self.sendMsg)
            iThread.daemon = True
            iThread.start()

            while True:
                data = self.sock.recv(1024)
                if not data:
                    break
                print(str(data, 'windows-1250'))

        except ConnectionRefusedError:
            print("connection refused \nmaybe the server isn't running?")


IP_ADDR = get_arguments()
if IP_ADDR:
    '''jeśli mamy podany adres ip, to jesteśmy klientem'''
    client = Client(IP_ADDR)
    pass
else:
    server = Server()
    server.run()

