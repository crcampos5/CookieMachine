import tkinter as tk
from tkinter import ttk
from core.cnc.cnc import Cnc
from gui.componentframe import ComponentFrame
from PIL import Image, ImageTk
import os
import cv2 as cv

class MoveFrame(ComponentFrame):
    def __init__(self,parent,cnc = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.cnc = cnc
        self.list_und = ['10 mm','1 mm','0.1 mm']
        self.selected_und = tk.StringVar(self)
        self.selected_und.set(self.list_und[0])

        img_left_move = ImageTk.PhotoImage(file= 'asset/left_move.png')
        img_bottom_move = ImageTk.PhotoImage(file= 'asset/bottom_move.png')
        img_right_move = ImageTk.PhotoImage(file= 'asset/right_move.png')
        img_top_move = ImageTk.PhotoImage(file= 'asset/top_move.png')

        btn_xplus = tk.Button(self,text='>',image=img_right_move,width=35,command=self.move_xplus)
        btn_xplus.image = img_right_move
        btn_xminus = tk.Button(self,text='<',image=img_left_move,width=35,command=self.move_xminus)
        btn_xminus.image = img_left_move
        btn_yplus = tk.Button(self,text='^',image=img_top_move,height=35,command=self.move_yplus)
        btn_yplus.image = img_top_move
        btn_yminus = tk.Button(self,text='v',image=img_bottom_move,height=35,command=self.move_yminus)
        btn_yminus.image = img_bottom_move
        btn_zplus = tk.Button(self,text='z+',image=img_top_move,height=35,command=self.move_zplus)
        btn_zplus.image = img_top_move
        btn_zminus = tk.Button(self,text='z-',image=img_bottom_move,height=35,command=self.move_zminus)
        btn_zminus.image = img_bottom_move

        lbl_und  = tk.Label(self, text='Unidad:',bg='gray90')
        cbx_und = ttk.Combobox(self,values=self.list_und,textvariable=self.selected_und,width=8)


        lbl_und.grid(row=0,column=0,columnspan=2,pady=10)
        cbx_und.grid(row=0,column=2,columnspan=3)
        btn_xplus.grid(row=2,column=2)
        btn_xminus.grid(row=2,column=0)
        btn_yplus.grid(row=1,column=1) 
        btn_yminus.grid(row=3,column=1) 
        btn_zplus.grid(row=1,column=3) 
        btn_zminus.grid(row=3,column=3)

        

        self.grid_propagate(0)
        self.config(width=170,height=180,bg='gray90')
    
    def set_cnc(self, cnc: Cnc):
        self.cnc = cnc

    def move_xplus(self):
        distance = self._get_distance()
        self.cnc.move('X',distance)

    def move_xminus(self):
        distance = self._get_distance()*-1
        self.cnc.move('X',distance)

    def move_yplus(self):
        distance = self._get_distance()
        self.cnc.move('Y',distance)

    def move_yminus(self):
        distance = self._get_distance()*-1
        self.cnc.move('Y',distance)

    def move_zplus(self):
        distance = self._get_distance()
        self.cnc.move('Z',distance)

    def move_zminus(self):
        distance = self._get_distance()*-1
        self.cnc.move('Z',distance)

    def _get_distance(self):
        valor_selected = self.selected_und.get()
        for und in self.list_und:
            if und == valor_selected:
                valor = float(und.split(" ")[0])
                break
        print(valor)
        return valor
    
    