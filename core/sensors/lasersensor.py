import math
import cv2 as cv
import threading

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
    def __init__(self,imagen):
        threading.Thread.__init__(self)
        self.imagen = imagen    
        #self.cap = None #cv.VideoCapture(1)
        self.exitcap = False
        
    def run(self):
        self.cap = cv.VideoCapture(2)
        print("Resolution w: ",self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("Resolution h: ",self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    def video(self):
        print('video laser')
        self.imagen.ban_stopvideo = False
        self.imagen.video(self.cap)

    def exit_video(self):
        self.imagen.ban_stopvideo = True

    def calculate_height(self,y):
        A = FGP * y + AMIN
        C = 180 - B - A
        a = c / math.sin(C) * math.sin(A) #Distancia desde el laser

    def process_image(self):
        self.imagen.cargar()
        img = self.imagen.imagen
        #
        #
        y = 240
        



    def isOpen(self):
        return self.cap.isOpened()

    def opencap(self):
        self.cap.open(2,cv.CAP_MSMF)

    def closecap(self):
        self.cap.release()


    

        
            
        
        