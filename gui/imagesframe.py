import tkinter as tk
from tkinter import ttk
from gui.componentframe import ComponentFrame
from PIL import Image, ImageTk
from models.imagen import Imagen

class ImagesFrame(ComponentFrame):
    def __init__(self,parent,imagen1 = None,imagen2 = None) -> None:
        super().__init__(parent)
        self.parent = parent

        img = ImageTk.PhotoImage(file= 'asset/noimage500x500.jpg')

        self.imagen1 = imagen1
        self.imagen2 = imagen2

        self.mode = tk.StringVar()
        self.mode.set("ambos")
        
        separador = ttk.Separator(self, orient="horizontal")
        self.lbl_imagen1 = ttk.Label(self,image=img)
        self.lbl_imagen1.image = img
        self.lbl_imagen2 = ttk.Label(self,image=img)
        self.lbl_imagen2.image = img

        
        camara = ttk.Radiobutton(self, text='Camara', variable=self.mode, value='camara',command=self.change_size)
        ambos = ttk.Radiobutton(self, text='Ambos', variable=self.mode, value='ambos',command=self.change_size)
        laser = ttk.Radiobutton(self, text='Laser', variable=self.mode, value='laser',command=self.change_size)

        separador.grid(row=0,column=0,columnspan=6, sticky="ew",padx=5,pady=5)
        camara.grid(row=1,column=0,columnspan=2)
        ambos.grid(row=1,column=2,columnspan=2)
        laser.grid(row=1,column=4,columnspan=2)
        self.change_size()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)

        #estilo = ttk.Style()
        #estilo.configure('miestilo.TLabel', foreground='red', background = "blue")
        #self.lbl_imagen2.config(style='miestilo.TLabel')


        self.grid_propagate(0)
        self.config(width=1005,height=640)
    
    def set_displays(self,img1: Imagen, img2: Imagen):
        self.imagen1 = img1
        self.imagen2 = img2
        self.imagen1.set_display(self.lbl_imagen1)
        self.imagen2.set_display(self.lbl_imagen2)

    def change_size(self):
        if self.mode.get() == "camara" :
            self.lbl_imagen2.grid_remove()
            self.lbl_imagen1.grid(row=2,column=0,padx=5,columnspan=6,sticky="ewsn")
            #self.columnconfigure(0, weight=1)
        elif self.mode.get() == "laser" :
            self.lbl_imagen1.grid_remove()
            self.lbl_imagen2.grid(row=2,column=0,columnspan=6,sticky="ewsn")
            #self.columnconfigure(0, weight=1)
        else :
            self.lbl_imagen1.grid(row=2,column=0,padx=5,columnspan=3,sticky="ewsn")
            self.lbl_imagen2.grid(row=2,column=3,columnspan=3,sticky="ewsn")

    

        
        