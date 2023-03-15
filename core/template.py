import math
import numpy as np
import cv2 as cv

from models.imagen import Imagen
from models.linegcode import LineGcode

class Template:

    def __init__(self,name, centro = None, ratio = None) -> None:
        self.name = name
        self.centro = centro
        self.ratio = ratio
        self.puntos = []
        self.base_gcode = []
        self.upload()
        self.generate_base()
        self.offset_angle = -35
        self.valormm = 3.2


    def upload(self):
        #carga un archivo segun el nombre
        ruta = "designs/bob_esponja/"
        self.file = open(ruta + self.name +'.gcode')
        lines = self.file.readlines()
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
        self.file.close()

    def generate_base(self):
        lines = self.file.readlines()
        for line in lines:
            self.base_gcode.append(LineGcode(line))

    #Genera el gcode incluyendo la posicion del 
    #cuadrante, coje cada linea y la mueve 

    def generate_gcode(self,quadrant):
        x,y = self.imagen.centro
        angle = self.imagen.angle
        x = x/self.valormm + quadrant[0]
        y = y/self.valormm + quadrant[1]

        cookie_gcode = self.base_gcode.copy()

        for line in cookie_gcode:
            line.move([x,y],angle)

        return cookie_gcode
        

    def move(self, points : list, position,angle):
        #esta funcion recibe una lista de puntos 
        # y los traslada en el plano a la 
        # posicion y angulo asignado
        l = []
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

    def draw_template(self,img):
        x,y = img.centro
        angle = img.angle
        print(x,y)
        p = self.move(self.puntos,(x/self.valormm,y/self.valormm),angle)
        self.puntos = self.convert_mm2pixel(p,self.valormm)

        #img = np.zeros((2000,1735,3), np.uint8)

        pts = np.array(self.puntos, np.int32)
        #pts = pts.reshape((-1,1,2))
        cv.polylines(img.imagen,[pts],True,(0,255,0),2)
        #cv.imshow('template',img)
        #cv.imwrite(self.name + '_template.jpg',img.imagen)

    def set_imagen(self, img : Imagen):
        self.imagen = img
  