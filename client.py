from socket import *
from random import *
from threading import *
from time import sleep
from tkinter import *


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

        thread_1 = Thread(target=self.receiveServerResponse, args=(
            identity, clientTcpSocket), daemon=True, name='ServerResponse')
        thread_1.start()

        self.clientWindow(clientTcpSocket)

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

    def clientWindow(self, clientTcpSocket):

        def receiveBroadcast(ClientTcpSocket, Broadcast):
            while True:
                broadcaseIdentity = ClientTcpSocket.recv(1024).decode()
                if (broadcaseIdentity == 'BROADCAST'):
                    userIdentity = ClientTcpSocket.recv(1024).decode()
                    message = ClientTcpSocket.recv(1024).decode()
                    print(f"{userIdentity} > {message}")
                    Broadcast.config(state='normal')
                    Broadcast.insert('end', f"{userIdentity} > {message}\n")
                    Broadcast.config(state='disabled')

        newClientWindow = Tk()
        newClientWindow.title("Texas Hold'Em Client")
        newClientWindow.geometry('1500x700+10+40')
        newClientWindow.resizable(False, False)

        cardsZone = Frame(newClientWindow, height=700,
                          width=1100, bd=10, bg='green', relief='sunken')
        cardsZone.grid(row=0, column=0)

        clientZone = Frame(newClientWindow, height=700,
                           width=400, bd=5, bg='gray', relief='sunken')
        clientZone.grid(row=0, column=1)
        clientZone.grid_propagate(False)
        broadcast = Text(clientZone, height=30, width=40,
                         bd=6, bg="darkgray", font=('宋体', 13), state='disabled')
        broadcast.grid(row=0, column=0, padx=6, pady=6)

        BroadcastThread = Thread(target=receiveBroadcast, args=(
            clientTcpSocket, broadcast), daemon=True, name='broadcast')
        BroadcastThread.start()

        newClientWindow.mainloop()


newPokerClient = PokerClient()
newPokerClient.run()
