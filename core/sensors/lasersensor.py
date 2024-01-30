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
FPG = FOV_V / RESOLUTION_H # Factor Pixel a Grados
AMIN = 43.83 #Angulo minimo
B = 90 # Angulo del laser 
c = 50 # Distancia de de laser a camara

class LaserSensor(threading.Thread):
    def __init__(self,imagen: Imagen, laser_number):
        threading.Thread.__init__(self)
        self.camera_matrix   = np.load('parameters/cam2/CameraMatrix.npy')
        self.camera_distortion   = np.load('parameters/cam2/DistMatrix.npy')
        self.imagen = imagen    
        self.imagen.set_matrix(self.camera_matrix,self.camera_distortion)
        self.laser_number = laser_number
        #self.cap = None #cv.VideoCapture(1)
        self.exitcap = False
        
    def run(self):
        self.cap = cv.VideoCapture(self.laser_number) 
        #self.cap.set(cv.CAP_PROP_FRAME_WIDTH,3264)
        #self.cap.set(cv.CAP_PROP_FRAME_HEIGHT,2448)
        print("Resolution laser w: ",self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("Resolution laser h: ",self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        
        self.cap.set(cv.CAP_PROP_BACKLIGHT,2)
        self.imagen.set_cap(self.cap)

    def video(self):
        print('video laser')
        self.imagen.ban_stopvideo = False
        self.imagen.video(self.cap)

    def exit_video(self):
        self.imagen.ban_stopvideo = True

    def calculate_height(self,y):
        FOV_V = 44.9 #Campo de vision vertical de la camara
        RESOLUTION_H = 480 #Resolucion vertical de la camara
        AMIN = 44.1 #Angulo minimo
        B = 90 # Angulo del laser 
        c = 50 # Distancia de de laser a camara
        
        B_cam = (180 - FOV_V) / 2
        c_cam = RESOLUTION_H / math.sin(math.radians(FOV_V)) * math.sin(math.radians(B_cam))

        y_b = math.sqrt(y**2 + c_cam**2 - 2*y*c_cam*math.cos(math.radians(B_cam)))

        y_A = math.degrees(math.asin(math.sin(math.radians(B_cam)) * y / y_b))

        x = c * math.tan(math.radians(y_A + AMIN))

        print("Distance: ", x)

    def process_image(self):
        self.cnc.laseronoff(True)
        time.sleep(1)
        print("Exposicion: ",self.cap.get(cv.CAP_PROP_EXPOSURE))
        acepto = self.cap.set(cv.CAP_PROP_EXPOSURE,-8)
        print(acepto)
        print("Exposicion: ",self.cap.get(cv.CAP_PROP_EXPOSURE))
        self.imagen.cargar()
        self.imagen.show()
        cv.imwrite('laser.jpg',self.imagen.imagen)
        img = self.imagen.imagen
        cv.imshow("Original",img)
        imageOut = img[0:480,213:426]
        
        img = cv.cvtColor(imageOut, cv.COLOR_RGB2GRAY)
        ret, image = cv.threshold(img, 70, 255, cv.THRESH_BINARY)


        cnts,_ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
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
        cv.imshow("img",image)
        self.imagen.imagen = image
        self.imagen.show()

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


    

        
            
        
        