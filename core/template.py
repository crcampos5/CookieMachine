import math
import numpy as np
import cv2 as cv

class Template:

    def __init__(self,name, centro = None, ratio = None) -> None:
        self.name = name
        self.centro = centro
        self.ratio = ratio
        self.puntos = []
        self.upload()
        self.offset_angle = -35


    def upload(self):
        #carga un archivo segun el nombre
        self.file = open(self.name +'.gcode')
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
        p = self.move(self.puntos,(x/13.35,y/13.35),angle)
        self.puntos = self.convert_mm2pixel(p,13.35)

        #img = np.zeros((2000,1735,3), np.uint8)

        pts = np.array(self.puntos, np.int32)
        #pts = pts.reshape((-1,1,2))
        cv.polylines(img.imagen,[pts],True,(0,255,0),10)
        #cv.imshow('template',img)
        cv.imwrite(self.name + '_template.jpg',img.imagen)
  