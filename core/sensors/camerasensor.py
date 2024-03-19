import cv2 as cv
import numpy as np
import threading

from models.imagen import Imagen


class CameraSensor(threading.Thread):

    def __init__(self, imagen: Imagen, camera_number):
        threading.Thread.__init__(self)
        # resolucion 3264 x 2448
        self.camera_matrix = np.load('parameters/cam2/CameraMatrix.npy')
        self.camera_distortion = np.load('parameters/cam2/DistMatrix.npy')
        self.imagen = imagen
        self.imagen.set_matrix(self.camera_matrix, self.camera_distortion)
        self.camera_number = camera_number
        self.resolution = [640, 480]
        self.cap = None
        self.c_captures = 0
        self.cnc = None

    def run(self):
        pass

    def video(self):
        print('video camera')
        if self.is_open() is False:
            self.open_camera()
        self.imagen.ban_stopvideo = False
        self.imagen.video(self.cap)

    def exit_video(self):
        self.imagen.ban_stopvideo = True

    def is_open(self):
        if self.cap is not None:
            return self.cap.isOpened()
        else:
            return False

    def capture(self):
        if self.is_open() == False:
            self.open_camera()
        ret = self.imagen.cargar()

        if ret:
            self.c_captures += 1
            img = self.imagen.imagen
            cv.imwrite("capture"+str(self.c_captures)+".jpg", img)

    def open_camera(self):
        self.cap = cv.VideoCapture(self.camera_number, cv.CAP_DSHOW)
        self.cap.set(cv.CAP_PROP_SETTINGS, 0.0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        print("Resolution W: ", self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("Resolution H: ", self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        # self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        # self.cap.set(cv.CAP_PROP_FPS, 15)
        self.imagen.set_cap(self.cap)
        self.imagen.set_mode("camera")
        q = 0
        # Se ejecuta el siguiente while para darle tiempo a la camara que
        # ajuste sus parametros
        while q < 3:
            ret, imagen = self.cap.read()
            gris = cv.cvtColor(imagen, cv.COLOR_BGR2GRAY)
            luminancia_media = cv.mean(gris)[0]
            print("Luminancia media de la imagen:", luminancia_media)
            q += 1
        self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        self.cap.set(cv.CAP_PROP_FOCUS, 208)

    def closecap(self):
        self.cap.release()

    def search_quadrant(self):
        print("search quadrant")
        self.imagen.activate_quadrant()

    def exit_quadrant(self):
        print("exit quadrant")

    def sweep_area(self):
        pass