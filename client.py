from socket import *
from random import *
from threading import *
from time import sleep
from tkinter import *
from base64 import b64decode


class PokerClient:
    SERVER_SIGNAL = ["BROADCAST", ]

    def run(self):
        self.connectionWindow()
        while True:
            try:
                domain = input("界面还没搓，在这里粘贴那串神奇的代码: ").encode()
                for i in range(4):
                    domain = b64decode(domain)
                clientTcpSocket = socket(AF_INET, SOCK_STREAM)
                serverAddress = (domain.decode(), 11451)
                print("Connecting...")
                clientTcpSocket.connect(serverAddress)
                # print(f"Connected to {serverAddress}")
                break
            except:
                print("Couldn't Connect to Server.")
                # sleep(15)
                continue

        alphabet = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        identity = ''
        for i in range(4):
            identity += alphabet[randint(0, len(alphabet)-1)]
        clientTcpSocket.send(identity.encode())

        self.clientWindow(clientTcpSocket)

    def connectionWindow(self):
        newConnectionWindow = Tk()
        newConnectionWindow.title("加入 Texas Hold'Em 派对")
        newConnectionWindow.geometry('400x250+600+250')
        newConnectionWindow.resizable(False, False)
        

        
        newConnectionWindow.mainloop()
        pass    

    def clientWindow(self, clientTcpSocket):
        def receiveBroadcast(ClientTcpSocket, Broadcast):
            while True:
                receiveContent = ClientTcpSocket.recv(1024).decode().split('##', 2)
                if (receiveContent[0] == 'BROADCAST'):
                    userIdentity = receiveContent[1]
                    message = receiveContent[2]
                    print(f"{userIdentity} > {message}")
                    Broadcast.config(state='normal')
                    Broadcast.insert('end', f"{userIdentity} > {message}\n")
                    Broadcast.config(state='disabled')

        def HandleSendMessage(event=None):
            if (clientInputBox.get('0.0', 'end')):
                message = clientInputBox.get('0.0', 'end')[0:-1]
                if (message):
                    clientTcpSocket.send(message.encode())
                clientInputBox.delete('0.0', 'end')
            return 'break'

        def HandleNewRow(event):
            clientInputBox.insert('end', '\n')
            return 'break'

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
        broadcast.grid(row=0, column=0, padx=8, pady=6,
                       columnspan=2, sticky='W')

        BroadcastThread = Thread(target=receiveBroadcast, args=(
            clientTcpSocket, broadcast), daemon=True, name='broadcast')
        BroadcastThread.start()

        clientInputBox = Text(clientZone, width=35, height=3,
                              bd=6, bg="darkgray", font=('宋体', 13))
        clientInputBox.bind("<Return>", HandleSendMessage)
        clientInputBox.bind("<Alt-Return>", HandleNewRow)
        clientInputBox.grid(row=1, column=0, sticky='E')
        sendBtn = Button(clientZone, width=4, height=3, bd=3,
                         bg="darkgray", text='发送\nEnter', command=HandleSendMessage)
        sendBtn.grid(row=1, column=1, ipadx=1)

        newClientWindow.mainloop()


newPokerClient = PokerClient()
newPokerClient.run()
