

import tkinter as tk


class Message:
    def __init__(self) -> None:
        self.message = ""

    def get(self):
        return self.message

    def set_console(self, console):
        self.console = console

    def insert(self, text):
        if (self.console != None):
            self.console.insert(tk.INSERT, text+"\n")
