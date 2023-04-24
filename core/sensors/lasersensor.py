import math
import time
import cv2 as cv
import threading
import numpy as np
from core.cnc.cnc import Cnc
from models.imagen import Imagen

# B____A
# |   /
#a|  /
# | /
# |/
# C

FOV_V = 45 #Campo de vision vertical de la camara
RESOLUTION_H = 480 #Resolucion vertical de la camara
FGP = FOV_V / RESOLUTION_H # Factor Grados a Pixel
AMIN = 37.5 #Angulo minimo
B = 90 # Angulo del laser 
c = 50 # Distancia de de laser a camara

class LaserSensor(threading.Thread):
    def __init__(self,imagen: Imagen):
        threading.Thread.__init__(self)
        self.camera_matrix   = np.load('parameters/cam2/CameraMatrix.npy')
        self.camera_distortion   = np.load('parameters/cam2/DistMatrix.npy')
        self.imagen = imagen    
        self.imagen.set_matrix(self.camera_matrix,self.camera_distortion)
        #self.cap = None #cv.VideoCapture(1)
        self.exitcap = False
        
    def run(self):
        self.cap = cv.VideoCapture(2)
        print("Resolution laser w: ",self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("Resolution laser h: ",self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.imagen.set_cap(self.cap)

    def video(self):
        print('video laser')
        self.imagen.ban_stopvideo = False
        self.imagen.video(self.cap)

    def exit_video(self):
        self.imagen.ban_stopvideo = True

    def calculate_height(self,y):
        A = FGP * y + AMIN
        C = 180 - B - A
       # sinc = math.sin(C)
        #print("Agulo C: ", C)
        #print("sin C: ", sinc)
        a = c / math.sin(math.radians(C)) * math.sin(math.radians(A)) #Distancia desde el laser
        print("Distance: ", a)

    def process_image(self):
        self.cnc.laseronoff(True)
        time.sleep(1)
        self.imagen.cargar()
        self.imagen.show()
        img = self.imagen.imagen
        imageOut = img[0:480,213:426]
        imageHSV = cv.cvtColor(imageOut, cv.COLOR_BGR2HSV)
        color_bajos = np.array([0, 0, 0], np.uint8)
        color_altos = np.array([146, 255, 255], np.uint8)
        color_bajos2 = np.array([0, 0, 221], np.uint8)
        color_altos2 = np.array([180, 11, 255], np.uint8)
        color_bajos3 = np.array([124, 0, 252], np.uint8)
        color_altos3 = np.array([180, 34, 255], np.uint8)
        image = cv.inRange(imageHSV, color_bajos3, color_altos3)
        image2 = cv.inRange(imageHSV, color_bajos2, color_altos2)
        #imageinv = cv.bitwise_not(image2)
        #im = cv.add(image2,image)
        kernel = np.ones((3,3),np.uint8)
        kernel2 = np.ones((4,4),np.uint8)
        dilation = cv.dilate(image,kernel,iterations = 1)
        #erode = cv.erode(image,kernel2,iterations = 1)
        cnts,_ = cv.findContours(image2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        print("No contornos: ", len(cnts))
        area = 0
        x = 0
        y = 0
        for c in cnts :
            a = cv.contourArea(c)
            if a > area : 
                area = a 
                m = cv.moments(c)
                x = m['m10']/m['m00']
                y = m['m01']/m['m00']
                
        print('x=',x, 'y=',y)
        self.calculate_height(y)
        #self.imagen.set(image)
        # self.imagen.show()
        #cv.imshow("img",image)
        #img = self.imagen.get()
        #print("No contornos: ", len(cnts))
        cv.imshow("img",image2)
        self.imagen.imagen = image2
        self.imagen.show()
        y = 240

    def measure_height(self):
        print("medir")
        self.process_image()

    def activate_laser(self):
        self.cnc.laseronoff(True)
        
        



    def isOpen(self):
        return self.cap.isOpened()

    def opencap(self):
        self.cap.open(2,cv.CAP_MSMF)

    def closecap(self):
        self.cap.release()

    def set_cnc(self, cnc: Cnc):
        self.cnc = cnc


    

        
            
        
        