from http import client
import socket
import threading
import pyaudio
import tkinter as tk
from tkinter import ttk
import signal
import sys

'''
def signal_handler(sig, frame):
    print('Send close message to server')
    sys.exit(0)
'''


class connToServer:

    def __init__(self):
        # make client a socket, and audio instance
        self.client = socket.socket()
        self.audio = pyaudio.PyAudio()

        # store server info
        self.host = "3.87.224.181"
        self.port = 5000

        self.username = ""
        
        # prepare streams
        self.Format = pyaudio.paInt16
        self.Chunks = 4096
        self.Channels = 1 # use mono audio so dont get problems with airpods etc (that split channels for input and output)
        self.Rate = 44100 #Hz

        self.input_stream = self.audio.open(format = self.Format,
                        channels = self.Channels,
                        rate = self.Rate,
                        input = True,
                        frames_per_buffer = self.Chunks)

        # passing audio to the server to pass to another client
        self.output_stream = self.audio.open(format = self.Format,
                            channels = self.Channels,
                            rate = self.Rate,
                            output = True,
                            frames_per_buffer = self.Chunks)

    def connect(self):
        self.client.connect((self.host,self.port))
    
    # send chunks of audio data to server
    def send(self):
        while(True):
            try:
                data = self.input_stream.read(self.Chunks)
                self.client.send(data)
            except:
                break

    # receive chunks of audio data from the server
    def receive(self):
        while(True):
            try:
                data = self.client.recv(self.Chunks)
                self.output_stream.write(data)
            except:
                break

    # close incoming audio stream
    def stopInputStream(self):
        self.input_stream.stop_stream()
        self.input_stream.close()

    # close outgoing audio stream
    def stopOutputStream(self):
        self.output_stream.stop_stream()
        self.output_stream.close()

    def passServerUsername(self, username):
        print("About to send ", username) 
        self.client.send(username.encode())
        self.username = username

    # close client
    def exit(self):

        # close audio connection
        self.audio.terminate()

        # close socket
        self.client.close()


class LoginScreen:
    def __init__(self, obj):
        self.serverConn = obj
        print(self.serverConn.host)
        self.screen = tk.Tk()
        self.username = "NULL"
        self.IP = 0

        self.screen.title("Login Screen")
        self.screen.geometry('400x200')

        user_label = ttk.Label(self.screen, text="Enter username", font=('Times new roman', 12))
        user_label.pack()

        self.user_text = tk.StringVar()
        user_entry = ttk.Entry(self.screen, textvariable=self.user_text)
        user_entry.pack()

        button = ttk.Button(self.screen, text="Enter", command=self.button_pressed)
        button.pack()

    def show_screen(self):
        self.screen.mainloop()

    def close_screen(self):
        self.screen.destroy()

    def button_pressed(self):
        self.username = self.user_text.get()

        # connect to the server
        self.serverConn.connect()
        self.serverConn.passServerUsername(self.username)

        if len(self.username) > 0:
            self.close_screen()
            chatbox = chatBox()
            chatbox.show_screen()

class chatBox:
    def __init__(self):
        self.screen = tk.Tk()

        self.screen.title("Chatbox")
        self.screen.geometry('800x500')

        message_label = ttk.Label(self.screen, text="Happy Chatting!")
        message_label.pack()

        self.main_box = tk.StringVar()
        self.box_entry = ttk.Entry(self.screen)
        self.box_entry.place(x=20, y=20, width=500, height=300)

        self.message = tk.StringVar()
        self.msg_entry = ttk.Entry(self.screen, textvariable=self.message)
        self.msg_entry.place(x=20, y=340, width=380, height=30)

        button = ttk.Button(self.screen, text="Send", command=self.send_message)
        button.place(x=420, y=340)

    def show_screen(self):
        self.screen.mainloop()

    def clear_input(self):
        self.msg_entry.delete(0, "end")

    def send_message(self):
        msg = self.message.get()
        self.box_entry.insert(tk.END, self.box_entry.get() + "\n" + msg + '\n')
        self.clear_input()


clientTest = connToServer()
login = LoginScreen(clientTest)
login.show_screen()
# signal.signal(signal.SIGINT, signal_handler)

try:
    

    # open a thread for sending voice data and receiving voice data
    t1 = threading.Thread(target = clientTest.send())
    t2 = threading.Thread(target = clientTest.receive())

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    clientTest.stopInputStream()
    clientTest.stopOutputStream()
    clientTest.exit()
except Exception as e:
    print(e)
