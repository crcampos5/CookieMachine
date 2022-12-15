import cv2 as cv
import numpy as np
import math
from core.template import Template

from models.imagen import Imagen

class BobEsponjaFace:
    def __init__(self) -> None:
       print("Clase bob esponja face")


    def execute(self,imagen : Imagen):
        self.imagen = imagen
        img = np.copy(self.imagen.imagen)
        #se convierte la imagen en hsv
        imageHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        #se crea los rangos de altos y bajos 
        color_bajos = np.array([0, 0, 0], np.uint8)
        color_altos = np.array([74, 255, 255], np.uint8)
        #la imagen queda convertida a binaria segun los rangos anteriores
        image = cv.inRange(imageHSV, color_bajos, color_altos)
        #se extrae los contornos de la imagen 
        cnts,_ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        #self.imagen.set(image)
       # self.imagen.show()
        #img = self.imagen.get()
        print("No contornos: ", len(cnts))
        for c in cnts:
            area = cv.contourArea(c)
            if area > 7000 and area < 2000000:
                print("area: ", area)
                    
                rect = cv.minAreaRect(c)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                #se aproxima los contornos a un poligono
                epsilon = 0.1*cv.arcLength(c,True)
                approx = cv.approxPolyDP(c,epsilon,True)
                cv.drawContours(img, [approx], 0, (0,0,255),10)
                self.imagen.set(img)
                self.imagen.show()
                #determinamos las lineas transversales del poligono 
                if approx.shape[0] == 4:   
                    x0,y0 = approx[0][0]
                    x1,y1 = approx[1][0]
                    x2,y2 = approx[2][0]
                    x3,y3 = approx[3][0]
                    d1 = math.sqrt((x2-x0)**2 + (y2-y0)**2)
                    d2 = math.sqrt((x3-x1)**2 + (y3-y1)**2)
                    #determinamos la linea mas larga
                    if d1 > d2:
                        a1,b1 = x0,y0
                        a2,b2 = x2,y2
                    else :  
                        a1,b1 = x1,y1
                        a2,b2 = x3,y3
                    #hallamos la pendiemte de la linea 
                    m = (b2*-1-b1*-1)/(a2-a1)
                    #determinamos el angulo de la galleta, esto nos permite saber 
                    #la rotacion de la galleta 
                    if(m > 0):
                        angle = math.degrees(math.atan(m))
                    else:  angle = math.degrees(math.atan(m)) + 180
                    self.imagen.angle = angle
                    print('Angle: ',angle)
                    #cv.line(img,(a1,b1),(a2,b2),(255,0,0),10)
                    #determinamos el momento del poligono para porterior mente obtener el centroide de la figura
                    m = cv.moments(approx)
                    x = m['m10']/m['m00']
                    y = m['m01']/m['m00']
                    print('x=',x, 'y=',y)
                    self.imagen.centro = (x,y)
                    #cv.circle(img, (int(x),int(y)), 5, 255, 5)
                        #self.imagen.set(img)
                    #self.imagen.show()
                    self.template = Template('bob_esponja_face')
        #self.template.draw_template(self.imagen)