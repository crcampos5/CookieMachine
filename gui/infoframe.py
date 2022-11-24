import tkinter as tk
from tkinter.font import BOLD
from gui.componentframe import ComponentFrame
from tkinter import scrolledtext
from models.message import Message
from PIL import Image, ImageTk
from models.position import Position

class InfoFrame(ComponentFrame):
    def __init__(self,parent,msg = None,pos = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.msg = msg 
        self.pos = pos

        img_x = ImageTk.PhotoImage(file= 'asset/xaxis.png')
        img_y = ImageTk.PhotoImage(file= 'asset/yaxis.png')
        img_z = ImageTk.PhotoImage(file= 'asset/zaxis.png')

        self.btn_X  = tk.Button(self, text='X:',image=img_x,font=("Verdana", 24,'bold'),command=self.homex,width=32)
        self.btn_X.image = img_x
        self.lbl_Xbox  = tk.Label(self, text=str(0.0),bg='white',width=14,font=("Verdana", 18))

        self.btn_Y  = tk.Button(self, text='Y:',image=img_y,font=("Verdana", 24,'bold'),command=self.homey,width=32)
        self.btn_Y.image = img_y
        self.lbl_Ybox  = tk.Label(self, text=str(0.0),bg='white',width=14,font=("Verdana", 18))

        self.btn_Z  = tk.Button(self, text='Z:',image=img_z,font=("Verdana", 24,'bold'),command=self.homez,width=32)
        self.btn_Z.image = img_z
        self.lbl_Zbox  = tk.Label(self, text=str(0.0),bg='white',width=14,font=("Verdana", 18))

        self.lbl_console  = scrolledtext.ScrolledText(self,wrap = tk.WORD,bg='white',width=28,height=23)

        

        self.btn_X.grid(row=0,column=0,padx=2,pady=1)
        self.lbl_Xbox.grid(row=0,column=1,padx=2,pady=1)

        self.btn_Y.grid(row=1,column=0,padx=2,pady=1)
        self.lbl_Ybox.grid(row=1,column=1,padx=2,pady=1)

        self.btn_Z.grid(row=2,column=0,padx=2,pady=1)
        self.lbl_Zbox.grid(row=2,column=1,padx=2,pady=1)

        self.lbl_console.grid(row=3,column=0,columnspan=2,padx=2,pady=2)

    def set_pos(self, pos: Position):
        self.pos = pos
        self.pos.set_displays(self.lbl_Xbox,self.lbl_Ybox,self.lbl_Zbox)
    
    def set_msg(self, msg: Message):
        self.msg = msg
        self.msg.set_console(self.lbl_console)
        self.msg.insert("Bienvenido")

    def homex(self):
        print("homex")

    def homey(self):
        pass

    def homez(self):
        pass







