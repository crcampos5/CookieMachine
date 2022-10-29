import tkinter as tk
from tkinter import ttk
from gui.componentframe import ComponentFrame
from PIL import Image, ImageTk
import os
import cv2 as cv

class MoveFrame(ComponentFrame):
    def __init__(self,parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.list_und = ['1 mm','0.1 mm']
        self.selected_und = tk.StringVar(self)
        self.selected_und.set(self.list_und[0])

        img_left_move = ImageTk.PhotoImage(file= 'asset/left_move.png')
        img_bottom_move = ImageTk.PhotoImage(file= 'asset/bottom_move.png')
        img_right_move = ImageTk.PhotoImage(file= 'asset/right_move.png')
        img_top_move = ImageTk.PhotoImage(file= 'asset/top_move.png')

        btn_xplus = tk.Button(self,text='>',image=img_right_move,width=35)
        btn_xplus.image = img_right_move
        btn_xminus = tk.Button(self,text='<',image=img_left_move,width=35)
        btn_xminus.image = img_left_move
        btn_yplus = tk.Button(self,text='^',image=img_top_move,height=35)
        btn_yplus.image = img_top_move
        btn_yminus = tk.Button(self,text='v',image=img_bottom_move,height=35)
        btn_yminus.image = img_bottom_move
        btn_zplus = tk.Button(self,text='z+',image=img_top_move,height=35)
        btn_zplus.image = img_top_move
        btn_zminus = tk.Button(self,text='z-',image=img_bottom_move,height=35)
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
       