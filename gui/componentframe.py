import tkinter as tk

#Clase padre de los frame 
class ComponentFrame(tk.Frame):

    def __init__(self,parent) -> None:
        tk.Frame.__init__(self,parent)
        self.parent = parent

    def process(self,e):
        pass