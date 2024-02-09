# La clase Template esta diseñado para manipular y transformar archivos G-code, 
# especialmente para trabajar con plantillas y generar nuevos G-codes a partir de ellas.

import math
import numpy as np
import cv2 as cv

from models.imagen import Imagen
from models.linegcode import LineGcode

class Template:

    def __init__(self,name, centro = None, ratio = None, ) -> None:
        self.name = name
        self.centro = centro
        self.ratio = ratio
        self.puntos = []
        self.base_gcode = []
        self.upload()
        self.extract_points()
        self.generate_base()
        self.offset_angle = 35 #Ángulo de compensación, inicializado en 35.
        self.valor_pixel_to_mm = 0

    #El método upload carga un archivo según el nombre proporcionado
    def upload(self):
        #carga un archivo segun el nombre
        ruta = "designs/bob_esponja/"
        self.file = open(ruta + self.name +'.gcode')
        self.lines = self.file.readlines()
        

    def extract_points(self):
        lines = self.lines.copy()
        #lee cada linea y guarda los puntos x y en un array
        for linea in lines:
            if 'G0' in linea or 'G1' in linea:
                if 'X' in linea:
                    l = linea.split('X')[1]
                    if 'Z' in l:
                        l = l.split('Z')
                        point = l[0].split('Y')
                        self.puntos.append((float(point[0]),float(point[1])))
                    elif 'F' in l:
                        l = l.split('F')
                        point = l[0].split('Y')
                        self.puntos.append((float(point[0]),float(point[1])))
                    else :
                        point = l.split('Y')
                        self.puntos.append((float(point[0]),float(point[1])))
        #self.file.close()

    def generate_base(self):
        #lines = self.file.readlines()
        for line in self.lines:
            self.base_gcode.append(LineGcode(line))
        self.file.close()
    #Genera el gcode incluyendo la posicion del 
    #cuadrante, coje cada linea y la mueve 

    def generate_gcode(self,centroide, valor_pixel_to_mm):
        self.valor_pixel_to_mm = valor_pixel_to_mm
        self.draw_template()
        angle = self.imagen.angle       

        cookie_gcode = self.base_gcode.copy()
        a = (angle - 90 + self.offset_angle) * -1
        angle = math.radians( a )
        print("Angulo Maquina: ", a)
        for line in cookie_gcode:
            line.move([centroide[0],centroide[1]],angle)

        return cookie_gcode
        

    def move(self, points : list, position,angle):
        #esta funcion recibe una lista de puntos 
        # y los traslada en el plano a la 
        # posicion y angulo asignado
        l = []
        #angle = math.radians(-1 * (angle - 90 + self.offset_angle))
        angle = math.radians(-1 * (angle - 90 + self.offset_angle))
        for p in points:
            x,y = p
            x1 = x * math.cos(angle) - y * math.sin(angle)
            y1 = x * math.sin(angle) + y * math.cos(angle) 
            x = x1 + position[0]
            y = y1 + position[1]
            l.append([x,y])
        return l

    def convert_mm2pixel(self, points, valor):
        #esta funcion convierte los puntos de milimetros a pixeles
        # multiplicando por el valor pasado por argumento 
        l = []
        for p in points:
            x,y = p
            x = round(x * valor)
            y = round(y * valor)
            l.append([x,y])
        return l

    def draw_template(self):
        x,y = self.imagen.centro
        angle = self.imagen.angle
        #self.puntos = self.base_gcode.copy()
        x1 = x/self.valor_pixel_to_mm
        y1 = y/self.valor_pixel_to_mm
        p = self.move(self.puntos,(x1,y1),angle)
        self.puntos = self.convert_mm2pixel(p,self.valor_pixel_to_mm)

        #img = np.zeros((2000,1735,3), np.uint8)

        pts = np.array(self.puntos, np.int32)
        #pts = pts.reshape((-1,1,2))
        cv.polylines(self.imagen.imagen,[pts],True,(0,255,0),2)
        self.imagen.show()
        #cv.imshow('template',img)
        #cv.imwrite(self.name + '_template.jpg',img.imagen)

    def set_imagen(self, img : Imagen):
        self.imagen = img
  