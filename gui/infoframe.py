import tkinter as tk
from tkinter.font import BOLD
from gui.componentframe import ComponentFrame
from tkinter import scrolledtext
from models.message import Message

from models.position import Position

class InfoFrame(ComponentFrame):
    def __init__(self,parent,msg = None,pos = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.msg = msg 
        self.pos = pos

        self.lbl_X  = tk.Label(self, text='X:',font=("Verdana", 24,'bold'))
        self.lbl_Xbox  = tk.Label(self, text=str(0.0),bg='white',width=14,font=("Verdana", 18))

        self.lbl_Y  = tk.Label(self, text='Y:',font=("Verdana", 24,'bold'))
        self.lbl_Ybox  = tk.Label(self, text=str(0.0),bg='white',width=14,font=("Verdana", 18))

        self.lbl_Z  = tk.Label(self, text='Z:',font=("Verdana", 24,'bold'))
        self.lbl_Zbox  = tk.Label(self, text=str(0.0),bg='white',width=14,font=("Verdana", 18))

        self.lbl_console  = scrolledtext.ScrolledText(self,wrap = tk.WORD,bg='white',width=28,height=23)

        

        self.lbl_X.grid(row=0,column=0,padx=2)
        self.lbl_Xbox.grid(row=0,column=1,padx=2)

        self.lbl_Y.grid(row=1,column=0,padx=2)
        self.lbl_Ybox.grid(row=1,column=1,padx=2)

        self.lbl_Z.grid(row=2,column=0,padx=2)
        self.lbl_Zbox.grid(row=2,column=1,padx=2)

        self.lbl_console.grid(row=3,column=0,columnspan=2,padx=2,pady=2)

    def set_pos(self, pos: Position):
        self.pos = pos
        self.pos.set_displays(self.lbl_Xbox,self.lbl_Ybox,self.lbl_Zbox)
    
    def set_msg(self, msg: Message):
        self.msg = msg
        self.msg.set_console(self.lbl_console)
        self.msg.insert("Bienvenido")







