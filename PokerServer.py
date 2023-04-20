from socket import *
from threading import *


class PokerServer:
    clients = dict()

    def run(self):
        serverTcpSocket = socket(AF_INET, SOCK_STREAM)
        serverTcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        serverAddress = ('', 11451)
        serverTcpSocket.bind(serverAddress)
        serverTcpSocket.listen(8)
        print(f"Server Running at localhost:{serverAddress[1]}...")
        while True:
            clientTcpSocket, _ = serverTcpSocket.accept()
            clientIdentity = clientTcpSocket.recv(256).decode()
            self.clients[clientIdentity] = clientTcpSocket
            print(f"{clientIdentity} joined the lobby.")
            thread = Thread(target=self.receive,
                            args=(clientTcpSocket, clientIdentity),
                            daemon=True,
                            name=f"{clientIdentity}")
            for client in self.clients.keys():
                    self.clients[client].send(
                        f"BROADCAST##[SERVER]##{clientIdentity} joined the lobby.".encode())
            thread.start()

    def receive(self, ClientTcpSocket, ClientIdentity):
        while True:
            try:
                clientMessage = ClientTcpSocket.recv(1024).decode()
            except ConnectionResetError:
                print(f"{ClientIdentity} left the lobby.")
                self.clients.pop(ClientIdentity)
                for client in self.clients.keys():
                    self.clients[client].send(
                        f"BROADCAST##[SERVER]##{ClientIdentity} left the lobby.".encode())
                break

            if clientMessage:
                print(f"{ClientIdentity} > {clientMessage}")

                for client in self.clients.keys():
                    self.clients[client].send(
                        f"BROADCAST##{ClientIdentity}##{clientMessage}".encode())
                # ClientTcpSocket.send("Received".encode())
            else:
                print(f"{ClientIdentity} left the lobby.")
                self.clients.pop(ClientIdentity)

                for client in self.clients.keys():
                    self.clients[client].send(
                        f"BROADCAST##[SERVER]##{ClientIdentity} left the lobby.".encode())
                ClientTcpSocket.close()
                break


if __name__ == '__main__':
    newPokerServer = PokerServer()
    newPokerServer.run()
