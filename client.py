import socket
import threading
import pyaudio
import tkinter as tk
from tkinter import ttk

class connToServer:
    # make client a socket, and audio instance
    client = socket.socket()
    audio = pyaudio.PyAudio()

    # store server info
    host = "3.87.224.181"
    port = 5000
    
    # connect to the server
    client.connect((host,port))
    
    # prepare streams
    Format = pyaudio.paInt16
    Chunks = 4096
    Channels = 2
    Rate = 44100 #Hz

    def prepAudioStreams(self):
        # incoming audio from other client passed through server
        input_stream = self.audio.open(format = self.Format,
                            channels = self.Channels,
                            rate = self.Rate,
                            input = True,
                            frames_per_buffer = self.Chunks)

        # passing audio to the server to pass to another client
        output_stream = self.p.open(format = self.Format,
                            channels = self.Channels,
                            rate = self.Rate,
                            output = True,
                            frames_per_buffer = self.Chunks)
    
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

    # close client
    def exit(self):

        # close audio connection
        self.audio.terminate()

        # close socket
        self.client.close()
    

class LoginScreen:
    def __init__(self):
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

        ip_label = ttk.Label(self.screen, text="Enter IP", font=('Times new roman', 12))
        ip_label.pack()

        self.ip_text = tk.StringVar()
        ip_entry = ttk.Entry(self.screen, textvariable=self.ip_text)
        ip_entry.pack()

        button = ttk.Button(self.screen, text="Enter", command=self.button_pressed)
        button.pack()

    def show_screen(self):
        self.screen.mainloop()

    def button_pressed(self):
        self.username = self.user_text.get()
        self.IP = self.ip_text.get()
        print(self.username)
        print(self.IP)


login = LoginScreen()
login.show_screen()

try:
    client = connToServer()
except:
    print("Server is not available at the moment. Please close the program and try again later")

# open a thread for sending voice data and receiving voice data
t1 = threading.Thread(target = client.send)
t2 = threading.Thread(target = client.receive)

t1.start()
t2.start()

t1.join()
t2.join()
