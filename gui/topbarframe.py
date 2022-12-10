import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import operator
from core.cnc.cnc import Cnc
from core.core import Core
from core.observer import Observer
from core.subject import Subject
from gui.componentframe import ComponentFrame

class TopBarFrame(ComponentFrame,Observer):
    def __init__(self,parent,cnc = None) -> None:
        super().__init__(parent)
        self.cnc = cnc
        self.activ_connection = False

        self.img_on = ImageTk.PhotoImage(file= 'asset/on.png')
        self.img_off = ImageTk.PhotoImage(file= 'asset/off.png')
        self.img_alarm = ImageTk.PhotoImage(file= 'asset/alarm.png')

        self.list_port = []
        self.selected_port = tk.StringVar(self)
        

        self.list_design = {}
        self.archivos = {}
        self.selected_design = tk.StringVar(self)
        self.selected_design.set('Ninguno')

        self.upload_desings()
        self.define_widgets()
        
        self.config(width=1250,height=35)
        self.grid_propagate(0)


    def set_cnc(self, cnc: Cnc):
        self.cnc = cnc

    def set_core(self, core : Core):
        self.core = core

    def update(self, subject: Subject) -> None:
        self.list_port = [subject.port]
        self.cbx_port.config(values = self.list_port)
        self.selected_port.set(self.list_port[0])

        if subject.alarm :
            self.btn_alarm.config(image = self.img_alarm)
            self.btn_alarm.image = self.img_alarm

    def upload_desings(self):
        
        dir_desings = "designs/"
        content = os.listdir(dir_desings)
        for f in content:
            ficheros = os.listdir(dir_desings+f+"/")
            for a in ficheros:
                if ".py" in a:
                    n = a.split(".")[0].replace("_"," ")
                    self.archivos[n] = dir_desings + f + "/" + a
        self.list_design = list(self.archivos.keys())


    def define_widgets(self):
        self.wrap1 = tk.Frame(self,width=600,height=30)
        self.wrap1.grid_propagate(0)

        self.lbl_port  = tk.Label(self.wrap1, text='Port:')
        self.cbx_port = ttk.Combobox(self.wrap1,values=self.list_port,textvariable=self.selected_port)

        self.btn_conect = tk.Button(self.wrap1,text='Conectar',command=self.connect,image=self.img_off,width=80,compound = tk.LEFT)
        self.btn_alarm = tk.Button(self.wrap1,text=' Unlock',command=self.disabled_lock,image=self.img_off,width=80,compound = tk.LEFT)
        self.btn_alarm.image = self.img_off
        self.lbl_design  = tk.Label(self, text='Diseño:')
        self.cbx_design = ttk.Combobox(self,values=self.list_design,textvariable=self.selected_design)
        self.cbx_design.bind('<<ComboboxSelected>>', self.select)
        self.lbl_port.grid(row=0,column=0,pady=2)
        self.cbx_port.grid(row=0,column=1,pady=2)
        self.wrap1.grid(row=0,column=0,sticky=tk.E,pady=5,padx=5)
        self.btn_conect.grid(row=0,column=2,pady=2,padx=5)
        self.btn_alarm.grid(row=0,column=3)

        self.lbl_design.grid(row=0,column=1,padx=5,pady=5)
        self.cbx_design.grid(row=0,column=2,pady=5,padx=5)

    
    def select(self,e):
        self.core.file = self.archivos[self.selected_design.get()]


    def disabled_lock(self):
        self.cnc.disable_alarm()
        self.btn_alarm.config(image = self.img_off)
        self.btn_alarm.image = self.img_off
    
    def connect(self):
        self.activ_connection = operator.not_(self.activ_connection)
        
        if self.activ_connection :
            self.cnc.connect_serial()
            self.btn_conect.config(image = self.img_on)
            self.btn_conect.image = self.img_on
        else:
            self.btn_conect.config(image = self.img_off)
            self.btn_conect.image = self.img_off
