
import threading
import socket

port = 5000
host = "0.0.0.0"

server = socket.socket()

server.bind((host,port))
server.listen(5)

clients = []
usernames = []

def start():
    while(True):
        # accept new client socket, store their socket
        clientSock, clientAddr = server.accept()
        print("Client connected on ", str(clientAddr))

        # add the client socket to the servers active connection list
        clients.append(clientSock)

        # start a new thread for the client that sends voice data
        clientThread = threading.Thread(target = send, args = (clientSock, ))
        clientThread.start()

def send(incomingConnection):
    try:
        while(True):
            data = incomingConnection.recv(4096)
            for client in clients:
                if client != incomingConnection:
                    client.send(data)
    except:
        print("Client disconnected")

start()
