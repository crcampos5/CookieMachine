import tkinter as tk
from tkinter import ttk
from gui import componentframe as cf

class TopBarFrame(cf.ComponentFrame):
    def __init__(self,parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.bg = 'red'

        self.list_port = ['COM1','COM2']
        self.selected_port = tk.StringVar(self)
        self.selected_port.set('Ninguno')

        self.list_design = ['Bob Esponja - Negro','Bob Esponja - Ojos']
        self.selected_design = tk.StringVar(self)
        self.selected_design.set('Ninguno')

        wrap1 = tk.Frame(self,width=600,height=30)
        wrap1.grid_propagate(0)
        #wrap2 = tk.Frame(self,bg='black',width=600,height=30)
        #wrap2.grid_propagate(0)
        

        lbl_port  = tk.Label(wrap1, text='Port:')
        cbx_port = ttk.Combobox(wrap1,values=self.list_port,textvariable=self.selected_port)
        btn_conect = tk.Button(wrap1,text='Conectar')

        lbl_design  = tk.Label(self, text='Diseño:')
        cbx_design = ttk.Combobox(self,values=self.list_design,textvariable=self.selected_design)

        wrap1.grid(row=0,column=0,sticky=tk.E,pady=5,padx=5)
        #wrap2.grid(row=0,column=1,sticky=tk.E)


        lbl_port.grid(row=0,column=0,pady=2)
        cbx_port.grid(row=0,column=1,pady=2)
        btn_conect.grid(row=0,column=2,pady=2,padx=5)

        lbl_design.grid(row=0,column=1,padx=5,pady=5)
        cbx_design.grid(row=0,column=2,pady=5,padx=5)

        self.config(width=1250,height=30)
        self.grid_propagate(0)
