import cv2 as cv
import numpy as np
import threading

from models.imagen import Imagen

class CameraSensor(threading.Thread):

    def __init__(self,imagen : Imagen):
        threading.Thread.__init__(self)
        #resolucion 3264 x 2448
        self.camera_matrix   = np.load('parameters/cam2/CameraMatrix.npy')
        self.camera_distortion   = np.load('parameters/cam2/DistMatrix.npy')
        self.imagen = imagen
        self.imagen.set_matrix(self.camera_matrix,self.camera_distortion)
        #self.cap = cv.VideoCapture(0)
        #self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 3264)
        #self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 2448)
        #self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        #self.cap.set(cv.CAP_PROP_FPS, 15)
        #self.imagen.set_cap(self.cap)
        self.exitcap = False

    def run(self):
        self.cap = cv.VideoCapture(2)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
        print("Resolution W: ",self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("Resolution H: ",self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        #self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        #self.cap.set(cv.CAP_PROP_FPS, 15)
        self.imagen.set_cap(self.cap)

    def video(self):
        print('video camera')
        self.imagen.ban_stopvideo = False
        self.imagen.video(self.cap)

    def exit_video(self):
        self.imagen.ban_stopvideo = True

    def isOpen(self):
        return self.cap.isOpened()

    def capture(self):
        #self.opencap()
        ret = self.imagen.cargar()
        if ret : 
            self.closecap() 
            return True
        else: 
            self.closecap()
            return False

    def opencap(self):
        self.cap.open(0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 1900)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        self.cap.set(cv.CAP_PROP_FPS, 15)

    def closecap(self):
        self.cap.release()
    