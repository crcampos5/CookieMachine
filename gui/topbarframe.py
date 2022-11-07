import tkinter as tk
from tkinter import ttk
from gui import componentframe as cf
from PIL import Image, ImageTk
import operator

class TopBarFrame(cf.ComponentFrame):
    def __init__(self,parent,cnc) -> None:
        super().__init__(parent)
        self.parent = parent
        self.cnc = cnc
        self.activ_lock = False
        self.activ_connection = False

        self.img_on = ImageTk.PhotoImage(file= 'asset/on.png')
        self.img_off = ImageTk.PhotoImage(file= 'asset/off.png')
        self.img_alarm = ImageTk.PhotoImage(file= 'asset/alarm.png')

        self.list_port = self.cnc.find_port()
        self.selected_port = tk.StringVar(self)
        self.selected_port.set(self.list_port[0])

        self.list_design = ['Bob Esponja - Negro','Bob Esponja - Ojos']
        self.selected_design = tk.StringVar(self)
        self.selected_design.set('Ninguno')

        wrap1 = tk.Frame(self,width=600,height=30)
        wrap1.grid_propagate(0)
        #wrap2 = tk.Frame(self,bg='black',width=600,height=30)
        #wrap2.grid_propagate(0)
        

        lbl_port  = tk.Label(wrap1, text='Port:')
        cbx_port = ttk.Combobox(wrap1,values=self.list_port,textvariable=self.selected_port)
        self.btn_conect = tk.Button(wrap1,text='Conectar',command=self.connect,image=self.img_off,width=80,compound = tk.LEFT)
        self.btn_alarm = tk.Button(wrap1,text=' Unlock',command=self.disabled_lock,image=self.img_off,width=80,compound = tk.LEFT)
        self.btn_alarm.image = self.img_off
        lbl_design  = tk.Label(self, text='Diseño:')
        cbx_design = ttk.Combobox(self,values=self.list_design,textvariable=self.selected_design)

        wrap1.grid(row=0,column=0,sticky=tk.E,pady=5,padx=5)
        #wrap2.grid(row=0,column=1,sticky=tk.E)


        lbl_port.grid(row=0,column=0,pady=2)
        cbx_port.grid(row=0,column=1,pady=2)
        self.btn_conect.grid(row=0,column=2,pady=2,padx=5)
        self.btn_alarm.grid(row=0,column=3)

        lbl_design.grid(row=0,column=1,padx=5,pady=5)
        cbx_design.grid(row=0,column=2,pady=5,padx=5)

        self.config(width=1250,height=35)
        self.grid_propagate(0)


    def disabled_lock(self):
        self.cnc.disable_alarm()
        self.activ_lock = operator.not_(self.activ_lock)
        if self.activ_lock :
            self.btn_alarm.config(image = self.img_alarm)
            self.btn_alarm.image = self.img_alarm
        else:
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
