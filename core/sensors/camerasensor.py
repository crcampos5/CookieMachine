import cv2 as cv
import numpy as np
import threading

from models.imagen import Imagen

class CameraSensor(threading.Thread):

    def __init__(self,imagen : Imagen, camera_number):
        threading.Thread.__init__(self)
        #resolucion 3264 x 2448
        self.camera_matrix   = np.load('parameters/cam2/CameraMatrix.npy')
        self.camera_distortion   = np.load('parameters/cam2/DistMatrix.npy')
        self.imagen = imagen
        self.imagen.set_matrix(self.camera_matrix,self.camera_distortion)
        self.camera_number = camera_number        
        self.resolution = [640 , 480] 
        #self.cap = cv.VideoCapture(0)
        #self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 3264)
        #self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 2448)
        #self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        #self.cap.set(cv.CAP_PROP_FPS, 15)
        #self.imagen.set_cap(self.cap)
        self.c_captures = 0

    def run(self):
        self.cap = cv.VideoCapture(self.camera_number)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        print("Resolution W: ",self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("Resolution H: ",self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        #self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        #self.cap.set(cv.CAP_PROP_FPS, 15)
        self.imagen.set_cap(self.cap)
        self.imagen.set_mode("camera")

    def video(self):
        print('video camera')
        self.imagen.ban_stopvideo = False
        self.imagen.video(self.cap)

    def exit_video(self):
        self.imagen.ban_stopvideo = True

    def isOpen(self):
        return self.cap.isOpened()

    def capture(self):
        if self.isOpen() == False:
            self.opencap()
        ret = self.imagen.cargar()

        if ret : 
            self.c_captures += 1
            img = self.imagen.imagen
            cv.imwrite("capture"+str(self.c_captures)+".jpg",img)

    def opencap(self):
        self.cap.open(self.camera_number)
        #self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        #self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        #self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        #self.cap.set(cv.CAP_PROP_FPS, 15)

    def closecap(self):
        self.cap.release()

    def search_quadrant(self):
        print("search quadrant")
        self.imagen.activate_quadrant()

    def exit_quadrant(self):
        print("exit quadrant")

    