import tkinter as tk
from tkinter.font import BOLD
from gui.componentframe import ComponentFrame
from tkinter import scrolledtext

class InfoFrame(ComponentFrame):
    def __init__(self,parent) -> None:
        super().__init__(parent)
        self.parent = parent

        lbl_X  = tk.Label(self, text='X:',font=("Verdana", 24,'bold'))
        lbl_Xbox  = tk.Label(self, text='0.000',bg='white',width=14,font=("Verdana", 18))

        lbl_Y  = tk.Label(self, text='Y:',font=("Verdana", 24,'bold'))
        lbl_Ybox  = tk.Label(self, text='0.000',bg='white',width=14,font=("Verdana", 18))

        lbl_Z  = tk.Label(self, text='Z:',font=("Verdana", 24,'bold'))
        lbl_Zbox  = tk.Label(self, text='000.000',bg='white',width=14,font=("Verdana", 18))

        lbl_console  = scrolledtext.ScrolledText(self,wrap = tk.WORD,bg='white',width=28,height=23)
        lbl_console.insert(tk.INSERT,'Console--------------------')

        lbl_X.grid(row=0,column=0,padx=2)
        lbl_Xbox.grid(row=0,column=1,padx=2)

        lbl_Y.grid(row=1,column=0,padx=2)
        lbl_Ybox.grid(row=1,column=1,padx=2)

        lbl_Z.grid(row=2,column=0,padx=2)
        lbl_Zbox.grid(row=2,column=1,padx=2)

        lbl_console.grid(row=3,column=0,columnspan=2,padx=2,pady=2)

        






