import tkinter as tk
from tkinter import ttk


class LoginScreen:
    def __init__(self):
        self.screen = tk.Tk()

    def show_screen(self):
        self.screen.mainloop()


login = LoginScreen()
login.show_screen()
