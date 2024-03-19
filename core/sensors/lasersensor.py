import math
import os
import time
from core.parametros import Parametros
import cv2 as cv
import threading
import numpy as np
from core.cnc.cnc import Cnc
from core.sensors.utilssensor import analyzing_image, calc_scan_matrix
from core.sensors.utilssensor import calculate_height, find_centroid
from core.sensors.utilssensor import find_middle_pixels, skeleton_media
from core.sensors.utilssensor import tecnica_rojos
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
        if self._initialized:
            return
        threading.Thread.__init__(self)
        self._initialized = True
        self.camera_matrix = np.load('parameters/cam2/CameraMatrix.npy')
        self.camera_distortion = np.load('parameters/cam2/DistMatrix.npy')
        self.imagen = None
        self.parametros = Parametros()
        self.laser_number = self.parametros.get_parametro("laser_number")
        self.cap = None
        self.distance = 0
        self.reds = np.array([[0, 100, 20],
                              [8, 255, 255],
                              [170, 100, 60],
                              [179, 255, 255]])
        self.binary_ban = False
        self.midline_enabled = False
        self.canal_r_ban = False
        self.umbral_binary = 70
        self.is_processed = False
        self.red_enabled = False
        self.laser_type = "line"

    def run(self):
        pass

    def set_imagen(self, imagen: Imagen):
        self.imagen = imagen
        self.imagen.set_matrix(self.camera_matrix, self.camera_distortion)

    def video(self):
        print('video laser')
        if self.is_open() is False:
            self.open_camera()

        self.cnc.laser_onoff(True)
        time.sleep(1)
        self.imagen.ban_stopvideo = False
        self.set_focus(272)
        self.imagen.video(self.cap, self.procesar_imagen)

    def stop_video(self):
        self.imagen.stop_video()
        self.close_camera()

    def _point_process(self):
        if self.laser_type == "point":
            try:
                if self.is_open() is False:
                    self.open_camera()

                self.cnc.laser_onoff(True)
                time.sleep(1)

                ret = self.imagen.cargar()
                if ret is False:
                    raise ValueError("No se pudo capturar la imagen")

                self.imagen.show()
                img = self.imagen.imagen

                self.distance, red_image = find_centroid(img)
                self.imagen.imagen = red_image
            except ValueError as error:
                self.cnc.laser_onoff(False)
                print(error)

    def measure_height(self):
        print("medir")
        ret = self._point_process()
        return ret

    def activate_laser(self):
        self.cnc.laser_onoff(True)

    def procesar_imagen(self, frame):
        if self.is_processed:
            # a_time = time.time()
            pixeles_medios = find_middle_pixels(frame, self.umbral_binary)

            img = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)

            for pixel in pixeles_medios:
                if pixel is not None:
                    img[pixel[1], pixel[0]] = [0, 255, 0]

            # c_time = time.time()
            # print("Tiempo c: ", (c_time - a_time))

            if self.midline_enabled:
                img = skeleton_media(img, frame)

            return img
        elif self.canal_r_ban:
            b, g, r = cv.split(frame)
            return r
        elif self.red_enabled:
            img = tecnica_rojos(frame)
            if self.midline_enabled:
                img = skeleton_media(img, frame)
            return img
        else:
            return frame

    def line_process(self, frame):
        b = 50  # Distancia de de laser a camara
        FOV_H = 60  # Campo de vision vertical de la camara
        RESOLUTION_H = 1600  # Resolucion horizontal de la camara
        if self.laser_type == "line":
            pixeles_medios = find_middle_pixels(frame, self.umbral_binary)
            shap = pixeles_medios.shape
            positions = np.zeros(shap)
            for pixel in pixeles_medios:
                if pixel is not None:
                    x = pixel[0]
                    y = pixel[1]

                    a = calculate_height(y)

                    c = math.sqrt(a**2 + b**2)
                    G = FOV_H/2
                    i_angle = 180 - G + 90

                    horizontal_resol_mm = 2 * \
                        (c * math.sin(math.radians(G)) /
                         math.sin(math.radians(i_angle)))

                    factor_pixel_mm = RESOLUTION_H / horizontal_resol_mm

                    h_x = x / factor_pixel_mm

                    positions[x] = (h_x, a)

    def sweep_scan(self, starting_point, distance=100):
        try:
            
            x = starting_point[0]
            y = starting_point[1]

            offset_xy = self.cnc.modes["Laser"]
            x_final = x + offset_xy[0]
            y_final = y + offset_xy[1]
            self.cnc.movexy(x, y, "Laser")

            while 1:
                a = self.cnc.pos.X
                b = self.cnc.pos.Y
                if int(a) == x_final and int(b) == y_final:
                    break

            if self.is_open() is False:
                self.open_camera()

            list_images = self.cnc.move_scan(
                (x + distance), y, self.cap, distance)
            
            self.save_images(list_images)
            matrix = calc_scan_matrix(list_images, self.umbral_binary)

            xnew = []
            ynew = []
            for i in range(196):
                xnew.append(i)
                ynew.append(matrix[50,i])

            plt.plot(xnew, ynew, '-')
            plt.show()

            X = np.arange(0, 100)
            Y = np.arange(0, 196)

            X, Y = np.meshgrid(X, Y)
            Z = []

            for i in range(100):
                aux_list = []
                for j in range(196):
                    aux_list.append(matrix[i, j])
                Z.append(aux_list)

            x = np.array(X)
            y = np.array(Y)
            z = np.transpose(np.array(Z))

            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            ax.plot_surface(x, y, z, rstride=1, cstride=1,
                            cmap='plasma', linewidth=1, antialiased=True)
            ax.set_zlim(0, 50)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")

            plt.show()
            # self.save_images(list_images)
        except ValueError as error:
            self.cnc.laser_onoff(False)
            self.cnc.stop()
            print(error)

    def sweep_scantest(self, starting_point, distance=100):
        try:
            list_images = []
            input_images_path = "imgtest"
            files_names = os.listdir(input_images_path)
            for file_name in files_names:
                # print(file_name)
                image_path = input_images_path + "/" + file_name
                image = cv.imread(image_path)
                list_images.append(image)

            matrix = calc_scan_matrix(list_images, self.umbral_binary)

            X = np.arange(0, 100)
            Y = np.arange(0, 196)

            X, Y = np.meshgrid(X, Y)
            Z = []

            for i in range(100):
                aux_list = []
                for j in range(196):
                    aux_list.append(matrix[i, j])
                Z.append(aux_list)

            x = np.array(X)
            y = np.array(Y)
            z = np.transpose(np.array(Z))

            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            ax.plot_surface(x, y, z, rstride=1, cstride=1,
                            cmap='viridis', linewidth=1, antialiased=True)
            # ax.scatter(xs, ys, zs,)
            ax.set_zlim(50, 170)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")

            plt.show()
        except ValueError as error:
            print(error)
            pass

    def scan_line(self, starting_position, distance=100):
        x = starting_position[0]
        y = starting_position[1]

        offset_xy = self.cnc.modes["Laser"]
        x_final = x + offset_xy[0]
        y_final = y + offset_xy[1]
        self.cnc.movexy(x, y, "Laser")
        while 1:
            a = self.cnc.pos.X
            b = self.cnc.pos.Y
            if int(a) == x_final and int(b) == y_final:
                break
        # for i in range(distance):
        list_images = self.cnc.move_scan((x + distance), y, self.cap, distance)
        list_height = []

        for img in list_images:

            h = analyzing_image(img)
            if h == 0:
                h = LASER_CERO
            list_height.append(LASER_CERO - h)
        print(list_height)

        _, ax = plt.subplots()
        ax.plot(range(distance), list_height)
        plt.show()
        # ret = self.measure_height()
        # print(self.distance)

    def is_open(self):
        if self.cap is not None:
            return self.cap.isOpened()
        else:
            return False

    def open_camera(self):
        self.cap = cv.VideoCapture(self.laser_number, cv.CAP_DSHOW)
        self.cap.set(cv.CAP_PROP_SETTINGS, 0.0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 1600)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1200)
        print("Resolution laser w: ", self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("Resolution laser h: ", self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0)
        # set exposure time
        self.cap.set(cv.CAP_PROP_EXPOSURE,
                     self.parametros.get_parametro("expositure"))
        print("Focus: ", self.cap.get(cv.CAP_PROP_FOCUS))
        # self.cap.set(cv.CAP_PROP_AUTOFOCUS, 1)
        # self.cap.set(cv.CAP_PROP_FOCUS, 272)
        # print("Focus2: ",self.cap.get(cv.CAP_PROP_FOCUS))

        if not self.cap.isOpened():
            print("Error al abrir la cámara")
            return False
        self.imagen.set_cap(self.cap)
        self.imagen.set_mode("laser")

        q = 0
        # Se ejecuta el siguiente while para darle tiempo a la camara que
        # ajuste sus parametros
        while q < 15:
            ret, imagen = self.cap.read()
            gris = cv.cvtColor(imagen, cv.COLOR_BGR2GRAY)
            luminancia_media = cv.mean(gris)[0]
            print("Luminancia media de la imagen:", luminancia_media)
            q += 1
        self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        self.cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 1)
        self.cap.set(cv.CAP_PROP_FOCUS, 272)
        self.cap.set(cv.CAP_PROP_EXPOSURE,
                     self.parametros.get_parametro("expositure"))
        print("Focus2: ", self.cap.get(cv.CAP_PROP_FOCUS))
        print("Expositure: ", self.cap.get(cv.CAP_PROP_EXPOSURE))
        return True

    def get_focus(self):
        f = self.cap.get(cv.CAP_PROP_FOCUS)
        print("Focus: ", f)
        return f

    def set_focus(self, focus):
        self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
        self.cap.set(cv.CAP_PROP_FOCUS, focus)
        print("Focus set: ", self.cap.get(cv.CAP_PROP_FOCUS))

    def close_camera(self):
        if self.cap is not None:
            self.cap.release()

    def set_cnc(self, cnc: Cnc):
        self.cnc = cnc

    def save_images(self, list_images):
        for i, img in enumerate(list_images):
            name = "imgtest/img_laser" + str(i) + ".jpg"
            cv.imwrite(name, img)
