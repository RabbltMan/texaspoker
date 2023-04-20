from socket import *
from random import *
from threading import *
from time import sleep

class PokerClient:
    SERVER_SIGNAL = ["BROADCAST", ]
    def run(self):
        clientTcpSocket = socket(AF_INET, SOCK_STREAM)
        serverAddress = ("127.0.0.1", 11451)

        print("Connecting...")
        while True:
            try:
                clientTcpSocket.connect(serverAddress)
                print(f"Connected to {serverAddress}")
                break
            except ConnectionRefusedError:
                print("Couldn't Connect to Server. Retry in 15s")
                sleep(15)
                continue

        alphabet = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        identity = ''
        for i in range(4):
            identity += alphabet[randint(0, len(alphabet)-1)]
        clientTcpSocket.send(identity.encode())

        thread = Thread(target=self.receiveBroadcast, args=(clientTcpSocket,), daemon=True)
        thread.start()
        self.receiveServerResponse(identity, clientTcpSocket)

    def receiveServerResponse(self, identity, clientTcpSocket):
        while True:
            sleep(0.1)
            request = input(f"{identity}: ")
            if (request):
                clientTcpSocket.send(request.encode())
                # serverResponse = clientTcpSocket.recv(1024)
                # print(f"[Server] {serverResponse.decode()}")
            else:
                continue

    def receiveBroadcast(self, clientTcpSocket):
        while True:
            broadcaseIdentity = clientTcpSocket.recv(1024).decode()
            if (broadcaseIdentity == 'BROADCAST'):
                userIdentity = clientTcpSocket.recv(1024).decode()
                message = clientTcpSocket.recv(1024).decode()
                print(f"{userIdentity} > {message}")

newPokerClient = PokerClient()
newPokerClient.run()