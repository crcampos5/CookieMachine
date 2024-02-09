import math
import time
import cv2 as cv
import threading
import numpy as np
from core.cnc.cnc import Cnc
from models.imagen import Imagen
import matplotlib.pyplot as plt

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
        self.distance = 0
        
    def run(self):
        self.cap = cv.VideoCapture(self.laser_number) 
        #self.cap.set(cv.CAP_PROP_FRAME_WIDTH,3264)
        #self.cap.set(cv.CAP_PROP_FRAME_HEIGHT,2448)
        print("Resolution laser w: ",self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("Resolution laser h: ",self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        
        self.cap.set(cv.CAP_PROP_BACKLIGHT,2)
        self.imagen.set_cap(self.cap)
        self.imagen.set_mode("laser")

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
        #self.distance = x
        #print("Distance: ", x)
        return x

    def process_image(self):
        if self.cap.isOpened() == False:
            self.cap.open(self.laser_number)
            self.cap.set(cv.CAP_PROP_BACKLIGHT,2)

        self.cnc.laseronoff(True)
        time.sleep(1)
        print("Exposicion: ",self.cap.get(cv.CAP_PROP_EXPOSURE))
        acepto = self.cap.set(cv.CAP_PROP_EXPOSURE,-8)
        print(acepto)
        print("Exposicion: ",self.cap.get(cv.CAP_PROP_EXPOSURE))
        ret = self.imagen.cargar()
        if ret :

            #self.cap.release()

            self.imagen.show()
            #cv.imwrite('laser.jpg',self.imagen.imagen)
            img = self.imagen.imagen
            #cv.imshow("Original",img)
            imageOut = img[0:480,213:426]
            self.imagen.imagen = imageOut
            self.imagen.show()
            red_image = self.red_technique(imageOut)
            #cv.imshow("Tecnica de rojos",red_image)
            #img = cv.cvtColor(imageOut, cv.COLOR_RGB2GRAY)
            #cv.imshow("Grises",img)
            #ret, image = cv.threshold(img, 70, 255, cv.THRESH_BINARY)


            cnts,_ = cv.findContours(red_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            print("No contornos: ", len(cnts))
            area = 0
            x = 0
            y = 0
            if len(cnts) :
                for c in cnts :
                    a = cv.contourArea(c)
                    if a > area : 
                        area = a 
                        m = cv.moments(c)
                        x = m['m10']/m['m00']
                        y = m['m01']/m['m00']

                print('x=',x, 'y=',y)
                if x != 0 and y != 0: 
                    self.calculate_height(y)
                    #cv.imshow("img",red_image)
                    self.imagen.imagen = red_image
                    #self.imagen.show()
                else: 
                    print("No se encontro ningun centro")
                    self.cnc.laseronoff(False)
                    return False
                    
            else : 
                print("No se encontraron contornos")
                self.cnc.laseronoff(False)
                return False
        else : 
            print("No se pudo tomar la imagen laser")
            self.cnc.laseronoff(False)
            return False
        self.cnc.laseronoff(False)
        return True

    def measure_height(self):
        print("medir")
        ret = self.process_image()
        return ret

    def activate_laser(self):
        self.cnc.laseronoff(True)
        
    def red_technique(self,frame):

        #redBajo1 = np.array([0, 100, 20], np.uint8)
        #redAlto1 = np.array([8, 255, 255], np.uint8)
        redBajo2=np.array([170, 100, 60], np.uint8)
        redAlto2=np.array([179, 255, 255], np.uint8)

        frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        #maskRed1 = cv.inRange(frameHSV, redBajo1, redAlto1)
        maskRed2 = cv.inRange(frameHSV, redBajo2, redAlto2)
        #maskRed = cv.add(maskRed1, maskRed2)

        return maskRed2
    
    def analyzing_image(self,frame):
        red_image = self.red_technique(frame)
        cnts,_ = cv.findContours(red_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        area = 0
        x = 0
        y = 0
        h = 0
        if len(cnts) :
            for c in cnts :
                a = cv.contourArea(c)
                if a > area : 
                    area = a 
                    m = cv.moments(c)
                    x = m['m10']/m['m00']
                    y = m['m01']/m['m00']
            if x != 0 and y != 0: 
                h = self.calculate_height(y)
        return h
    
    def scan_line(self, starting_position,distance = 100):
        x = starting_position[0]
        y = starting_position[1]
        self.cnc.movexy(x,y,"Laser")
        while 1:
            a = self.cnc.pos.X
            b = self.cnc.pos.Y
            if int(a) == -921 and int(b) == -255 :
                break
        #for i in range(distance):
        list_images = self.cnc.move_scan((x+100),y, self.cap)
        list_height = []
        laser_cero = 170.99
        for img in list_images:
            
            h = self.analyzing_image(img)
            if h == 0 : h = laser_cero
            list_height.append(laser_cero - h)
        print(list_height)

        
        fig, ax = plt.subplots()
        ax.plot(range(100), list_height)
        plt.show()
           # ret = self.measure_height()
            #print(self.distance)
        



    def isOpen(self):
        return self.cap.isOpened()

    def opencap(self):
        self.cap.open(2,cv.CAP_MSMF)

    def closecap(self):
        self.cap.release()

    def set_cnc(self, cnc: Cnc):
        self.cnc = cnc


    

        
            
        
        