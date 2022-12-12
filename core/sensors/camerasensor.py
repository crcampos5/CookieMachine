import cv2 as cv
import numpy as np

from models.imagen import Imagen

class CameraSensor:

    def __init__(self,imagen : Imagen) -> None:
        #resolucion 3264 x 2448
        self.camera_matrix   = np.load('parameters/cam1/CameraMatrix.npy')
        self.camera_distortion   = np.load('parameters/cam1/DistMatrix.npy')
        self.imagen = imagen
        self.imagen.set_matrix(self.camera_matrix,self.camera_distortion)
        self.cap = cv.VideoCapture(0,cv.CAP_DSHOW)
        self.cap.set(3, 1600)
        self.cap.set(4, 1200)
        #self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        self.imagen.set_cap(self.cap)
        self.exitcap = False

    def video(self):
        print('video camera')
        self.imagen.ban_stopvideo = False
        self.imagen.video(self.cap)

    def exit_video(self):
        self.imagen.ban_stopvideo = True

    def isOpen(self):
        return self.cap.isOpened()

    def capture(self):
        ret = self.imagen.cargar()
        if ret : return True
        else: False

    