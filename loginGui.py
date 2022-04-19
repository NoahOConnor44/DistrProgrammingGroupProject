import tkinter as tk
from tkinter import ttk


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


if __name__ == "__main__":
    login = LoginScreen()
    login.show_screen()
