

import math
import cv2 as cv
import numpy as np
from skimage.morphology import medial_axis


def calculate_height(d):
        FOV_V = 44.9 #Campo de vision vertical de la camara
        RESOLUTION_V = 1200 #Resolucion vertical de la camara
        RESOLUTION_H = 1600 #Resolucion horizontal de la camara
        AMIN = 44.1 #Angulo minimo
        C = 90 # Angulo del laser 
        b = 50 # Distancia de de laser a camara
        
        F = (180 - FOV_V) / 2
        e = RESOLUTION_V / math.sin(math.radians(FOV_V)) * math.sin(math.radians(F))

        f = math.sqrt(d**2 + e**2 - 2*d*e*math.cos(math.radians(F)))

        D = math.degrees(math.asin(math.sin(math.radians(F)) * d / f))

        a = b * math.tan(math.radians(D + AMIN))
        #self.distance = x
        #print("Distance: ", x)
        return a

def calculate_resolution_h(a):
        FOV_H = 60 #Campo de vision horizontal de la camara
        b = 50 # Distancia de de laser a camara
        H = 90

        c = math.sqrt(a**2 + b**2)
        G = FOV_H / 2 
        I = 180 - G + H

        mm_h = 2(c * math.sin(math.radians(G)) / math.sin(math.radians(I)))

        print("Milimetros Horizontales: ", mm_h)
        return mm_h


def red_technique(frame):

        #redBajo1 = np.array([0, 100, 20], np.uint8)
        #redAlto1 = np.array([8, 255, 255], np.uint8)
        redBajo2=np.array([170, 100, 60], np.uint8)
        redAlto2=np.array([179, 255, 255], np.uint8)

        frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        #maskRed1 = cv.inRange(frameHSV, redBajo1, redAlto1)
        maskRed2 = cv.inRange(frameHSV, redBajo2, redAlto2)
        #maskRed = cv.add(maskRed1, maskRed2)

        return maskRed2


def analyzing_image(frame):
        red_image = red_technique(frame)
        cnts,_ = cv.findContours(red_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        area = 0
        x = 0
        y = 0
        h = 0
        if len(cnts) :
            for c in cnts :
                a = cv.contourArea(c)
                if a > area : 
                    area = a 
                    m = cv.moments(c)
                    x = m['m10']/m['m00']
                    y = m['m01']/m['m00']
            if x != 0 and y != 0: 
                h = calculate_height(y)
        return h

def tecnica_rojos(frame,reds):
        frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        maskRed1 = cv.inRange(frameHSV, reds[0], reds[1])
        maskRed2 = cv.inRange(frameHSV, reds[2], reds[3])
        maskRed = cv.add(maskRed1, maskRed2)

        return maskRed

def skeleton_media(img,frame):
        skeleton = medial_axis(img)
        skeleton = skeleton.astype(np.uint8) * 255
        #frame = frame.astype(np.uint8) * 255
        frame[skeleton == 255] = [0, 255, 0]
        return frame