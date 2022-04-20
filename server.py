import threading
import socket

port = 5000
host = "0.0.0.0"

server = socket.socket()

server.bind((host,port))
server.listen(5)

clients = []

def start():
    while(True):
        conn, addr = server.accept()
        clients.append(conn)
        clientThread = threading.Thread(target = send, args = (conn, ))
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
