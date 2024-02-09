from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
import time

class Imagen:

    def __init__(self, display = None) -> None:
        self.name = None
        self.ban_stopvideo = False
        self.display = display
        self.angle = 0
        self.centro = (0,0)
        self.mode = None

    def cargar(self):
       # while self.cap.isOpened():
            print("camara abierta")
            #time.sleep(1)
            ret, imagen = self.cap.read()
            if ret == True:    
                self.imagen = imagen
                #cv.imshow("img",self.imagen)
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

    def set_mode(self,mode):
        self.mode = mode
    
    def show(self):
        
        imagen_display = cv.cvtColor(self.imagen, cv.COLOR_BGR2RGB)
        if self.mode == "camera" : 
            resolution = (480,640)
            imagen_display =cv.rotate(imagen_display, cv.ROTATE_90_COUNTERCLOCKWISE)
        else:  resolution = (213,480)
        imagensmall = cv.resize(imagen_display,resolution, interpolation=cv.INTER_CUBIC)
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

    def activate_quadrant(self):
        if (self.cap.isOpened()):
            ret, imagen = self.cap.read()
            if ret == True:
                
                self.imagen = imagen  #Falta distorcion
                cv.rectangle(self.imagen,(318,238),(322,242),(0,255,0),-1) # punto en centro 
                cv.rectangle(self.imagen,(83,35),(557,445),(0,255,0),1) # cuadrado grande
                self.show()
                self.display.after(10, self.activate_quadrant)
            else: self.cap.release()
        else: print('camera is close')


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
    
   