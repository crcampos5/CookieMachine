import math
import time
from core.parametros import Parametros
import cv2 as cv
import threading
import numpy as np
from core.cnc.cnc import Cnc
from core.sensors.utilssensor import analyzing_image, calculate_height, red_technique, skeleton_media, tecnica_rojos
from models.imagen import Imagen
import matplotlib.pyplot as plt




LASER_CERO = 170.99

class LaserSensor(threading.Thread):
    
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
            if self._initialized: return
            threading.Thread.__init__(self)
            self._initialized = True
            self.camera_matrix   = np.load('parameters/cam2/CameraMatrix.npy')
            self.camera_distortion   = np.load('parameters/cam2/DistMatrix.npy') 
            self.imagen = None
            self.parametros = Parametros()
            self.laser_number = self.parametros.get_parametro("laser_number")
            self.cap = None 
            self.distance = 0
            self.reds = np.array([0, 100, 20]
                                [8, 255, 255]
                                [170, 100, 60]
                                [179, 255, 255])
            self.binary_ban = False
            self.midline_enabled = False
            self.canal_r_ban = False
            self.umbral_binary = 90
            self.is_processed = False
            self.red_enabled = False
                  
        
    def run(self):
        pass

    def set_imagen(self, imagen: Imagen):
        self.imagen = imagen 
        self.imagen.set_matrix(self.camera_matrix,self.camera_distortion)

    def video(self):
        print('video laser')
        if self.is_open() is False:
            self.open_camera()

        self.cnc.laser_onoff(True)
        time.sleep(1)
        self.imagen.ban_stopvideo = False
        self.set_focus(272)
        self.imagen.video(self.cap,self.procesar_imagen)

    def stop_video(self):
        self.imagen.stop_video()
        self.close_camera()

    #def exit_video(self):
    #    self.imagen.ban_stopvideo = True

    def _process_image(self):
        if self.is_open() is False:
            self.open_camera()

        self.cnc.laser_onoff(True)
        time.sleep(1)

        ret = self.imagen.cargar()
        if ret :

            #self.cap.release()

            self.imagen.show()
            #cv.imwrite('laser.jpg',self.imagen.imagen)
            img = self.imagen.imagen
            #cv.imshow("Original",img)
            #imageOut = img[0:480,213:426]
            self.imagen.imagen = img
            self.imagen.show()
            red_image = red_technique(img)
            cv.imshow("Tecnica de rojos",red_image)
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
                    self.distance = calculate_height(y)
                    #cv.imshow("img",red_image)
                    self.imagen.imagen = red_image
                    #self.imagen.show()
                else: 
                    print("No se encontro ningun centro")
                    self.cnc.laser_onoff(False)
                    return False
                    
            else : 
                print("No se encontraron contornos")
                self.cnc.laser_onoff(False)
                return False
        else : 
            print("No se pudo tomar la imagen laser")
            self.cnc.laser_onoff(False)
            return False
        #self.cnc.laser_onoff(False)
        return True

    def measure_height(self):
        print("medir")
        ret = self._process_image()
        return ret

    def activate_laser(self):
        self.cnc.laser_onoff(True)
    
    def procesar_imagen(self,frame):
        if self.is_processed:
            #a_time = time.time()
            _, _, img = cv.split(frame)
            ret,img = cv.threshold(img,self.umbral_binary,255,cv.THRESH_BINARY)

            img = cv.GaussianBlur(img,(1,1),0)

            kernel = np.ones((3,3),np.uint8)
            img = cv.dilate(img,kernel,iterations = 1)
            img = cv.erode(img,kernel,iterations = 1)

            alto, ancho = img.shape
            pixeles_medios = [None] * ancho


            for col in range(ancho):
                columna = img[:, col]
                max = np.argmax(columna)
                columna = np.flip(columna)
                min = alto - np.argmax(columna)
                if max > 0 and min > 0:
                    pixel_medio = (col, int((max + min) / 2))
                    pixeles_medios[col] = pixel_medio

            
            img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)

            for pixel in pixeles_medios :
                if pixel is not None:
                    img[pixel[1], pixel[0]] = [0, 255, 0]
            

            
            #c_time = time.time()
            #print("Tiempo c: ", (c_time - a_time))

            if self.midline_enabled :
               img = skeleton_media(img,frame)

            return img
        elif self.canal_r_ban :
            b, g, r = cv.split(frame)
            return r
        elif self.red_enabled :
            img = tecnica_rojos(frame)  
            if self.midline_enabled :
                img = skeleton_media(img,frame)
            return img
        else: return frame
        
    
    def scan_line(self, starting_position,distance = 100):
        x = starting_position[0]
        y = starting_position[1]

        offset_xy = self.cnc.modes["Laser"]
        x_final = x + offset_xy[0]
        y_final = y + offset_xy[1]
        self.cnc.movexy(x,y,"Laser")
        while 1:
            a = self.cnc.pos.X
            b = self.cnc.pos.Y
            if int(a) == x_final and int(b) == y_final :
                break
        #for i in range(distance):
        list_images = self.cnc.move_scan((x + distance),y, self.cap, distance)
        list_height = []
        
        for img in list_images:
            
            h = analyzing_image(img)
            if h == 0 : h = LASER_CERO
            list_height.append(LASER_CERO - h)
        print(list_height)

        
        fig, ax = plt.subplots()
        ax.plot(range(distance), list_height)
        plt.show()
           # ret = self.measure_height()
            #print(self.distance)
        
    def is_open(self):
        if self.cap is not None :
            return self.cap.isOpened()
        else: return False

    def open_camera(self):
        self.cap = cv.VideoCapture(self.laser_number, cv.CAP_DSHOW) 
        self.cap.set(cv.CAP_PROP_SETTINGS,0.0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH,1600)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT,1200)
        print("Resolution laser w: ",self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("Resolution laser h: ",self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 1)
        # set exposure time
        self.cap.set(cv.CAP_PROP_EXPOSURE, self.parametros.get_parametro("expositure"))
        print("Focus: ",self.cap.get(cv.CAP_PROP_FOCUS))
        #self.cap.set(cv.CAP_PROP_AUTOFOCUS, 1)
        #self.cap.set(cv.CAP_PROP_FOCUS, 272)
        #print("Focus2: ",self.cap.get(cv.CAP_PROP_FOCUS))

        if not self.cap.isOpened():
            print("Error al abrir la cámara")
            return False
        self.imagen.set_cap(self.cap)
        self.imagen.set_mode("laser")

        q = 0
        # Se ejecuta el siguiente while para darle tiempo a la camara que ajuste sus parametros 
        while q < 15:            
            ret, imagen = self.cap.read()            
            q += 1
        self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        self.cap.set(cv.CAP_PROP_FOCUS, 272)
        print("Focus2: ",self.cap.get(cv.CAP_PROP_FOCUS))
        return True
    
    def get_focus(self):
        f = self.cap.get(cv.CAP_PROP_FOCUS)
        print("Focus: ",f)
        return f
    
    def set_focus(self,focus):
        self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        self.cap.set(cv.CAP_PROP_FOCUS, focus)
        print("Focus set: ",self.cap.get(cv.CAP_PROP_FOCUS))

    def close_camera(self):
        if self.cap is not None: 
            self.cap.release()

    def set_cnc(self, cnc: Cnc):
        self.cnc = cnc


    

        
            
        
        