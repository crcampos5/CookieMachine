from PIL import Image, ImageTk
import numpy as np
import cv2 as cv

class Imagen:

    def __init__(self, display = None) -> None:
        self.name = None
        self.ban_stopvideo = False
        self.display = display
        self.angle = 0
        self.centro = (0,0)
        self.cargar()

    def cargar(self):
        pass
        #self.imagen = cv.imread(name)

    
    def set(self, imagen):
        self.imagen = imagen
    
    def set_display(self,display):
        self.display = display
    
    def show(self):
        imagen_display = cv.cvtColor(self.imagen, cv.COLOR_BGR2RGB)
        imagensmall = cv.resize(imagen_display,(500,500), interpolation=cv.INTER_CUBIC)
        imagensmall = Image.fromarray(imagensmall)
        imagensmall = ImageTk.PhotoImage(imagensmall)
        if self.display != None :
            self.display.configure(image=imagensmall)
            self.display.image = imagensmall
        else: print('Display no definido')

    def _show2(self):
        if (self.cap.isOpened() and self.ban_stopvideo != True):
            ret, imagen = self.cap.read()
            if ret == True:
                
                self.imagen = imagen
                self.show()
                self.display.after(10, self._show2)
            else: self.cap.release()
        else: print('close')

    def video(self,cap):
        self.cap = cap
        self.display.after(10, self._show2)
    
   