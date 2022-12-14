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
        #self.cargar()

    def cargar(self):
        while self.cap.isOpened():
            print("camara abierta")
            ret, imagen = self.cap.read()
            if ret == True:    
                self.imagen = imagen
                cv.imshow("img",self.imagen)
                h,  w = self.imagen.shape[:2]
                print(h,w)
                self.undistorted_image()
                self.show()
                return True
            else: 
                self.cap.release()
                return False
        

    def set_cap(self,cap):
        self.cap = cap
    
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

    def undistorted_image(self): 
        #------------------------------#
        #--- Undistort the image using the camera calibration parameters
        h,  w = self.imagen.shape[:2]
        #if Show_All==1: print("[INFO] H: ", h, "   w: ", w)
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(self.camera_matrix, self.camera_distortion, (w,h), 1, (w,h))
        #if Show_All==1: print("[INFO] newcameramtx: \n",newcameramtx,"\n roi: \n ",roi)

        #--- Undistort
        undistorted_img = cv.undistort(self.imagen.copy(), self.camera_matrix, self.camera_distortion, None, newcameramtx)
        self.imagen = undistorted_img

    def set_matrix(self,matrix,distortion):
        self.camera_matrix   = matrix
        self.camera_distortion = distortion
    
   