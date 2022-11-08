import tkinter as tk
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
        

        self.lbl_imagen1 = tk.Label(self,bg='white',width=500,image=img)
        self.lbl_imagen1.image = img
        self.lbl_imagen2 = tk.Label(self,bg='white',width=500,image=img)
        self.lbl_imagen2.image = img

        #self.imagen1.set_display(lbl_imagen1)
        #self.imagen2.set_display(lbl_imagen2)

        self.lbl_imagen1.grid(row=0,column=0,padx=5)
        self.lbl_imagen2.grid(row=0,column=1)


        self.grid_propagate(0)
        self.config(width=1005,height=500)
    
    def set_displays(self,img1: Imagen, img2: Imagen):
        self.imagen1 = img1
        self.imagen2 = img2
        self.imagen1.set_display(self.lbl_imagen1)
        self.imagen2.set_display(self.lbl_imagen2)

    

        
        