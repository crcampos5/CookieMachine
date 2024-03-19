

import math
import cv2 as cv
import numpy as np
from skimage.morphology import medial_axis
from scipy import interpolate
import matplotlib.pyplot as plt

RESOLUTION_H = 1600  # Resolucion horizontal de la camara


def calculate_height(d):
    FOV_V = 44.9  # Campo de vision vertical de la camara
    RESOLUTION_V = 1200  # Resolucion vertical de la camara

    AMIN = 42.25  # Angulo minimo
    # C = 90  # Angulo del laser
    b = 57.81  # Distancia de de laser a camara

    F = math.radians((180 - FOV_V) / 2)
    e = RESOLUTION_V / math.sin(math.radians(FOV_V)) * math.sin(F)

    f = math.sqrt(d**2 + e**2 - 2*d*e*math.cos(F))

    D = math.degrees(math.asin(math.sin(F) * d / f))

    a = b * math.tan(math.radians(D + AMIN))
    # self.distance = x
    # print("Distance: ", x)
    return a


def calculate_resolution_h(a):
    FOV_H = 60  # Campo de vision horizontal de la camara
    b = 57.81  # Distancia de de laser a camara
    H = 90

    c = math.sqrt(a**2 + b**2)
    G = FOV_H / 2
    i_angle = 180 - G + H

    mm_h = 2 * (c * math.sin(math.radians(G)) /
                math.sin(math.radians(i_angle)))

    print("Milimetros Horizontales: ", mm_h)
    return mm_h


def convert_pixel_mm(pixel):
    x, y = pixel

    z_mm = calculate_height(y)
    # resol = calculate_resolution_h(z_mm)
    resol = 196
    y_mm = resol / RESOLUTION_H * x

    return y_mm, z_mm


def calc_scan_matrix(list_images, umbral_binary):

    matrix = np.zeros((100, 196), dtype=np.float)
    d_zero, yzero = get_zero(list_images[0], umbral_binary)
    for x, imagen in enumerate(list_images):
        pixeles_medios = find_middle_pixels(imagen, umbral_binary, x, yzero)
        z = 0
        y = 0
        for i, pixel in enumerate(pixeles_medios):
            y, z = convert_pixel_mm(pixel)
            #if z < 60:
            #    z = 163
            matrix[x, int(y)] = d_zero - z

    return matrix


def red_technique(frame):

    # redBajo1 = np.array([0, 100, 20], np.uint8)
    # redAlto1 = np.array([8, 255, 255], np.uint8)
    redBajo2 = np.array([170, 100, 60], np.uint8)
    redAlto2 = np.array([179, 255, 255], np.uint8)

    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # maskRed1 = cv.inRange(frameHSV, redBajo1, redAlto1)
    maskRed2 = cv.inRange(frameHSV, redBajo2, redAlto2)
    # maskRed = cv.add(maskRed1, maskRed2)

    return maskRed2


def analyzing_image(frame):
    red_image = red_technique(frame)
    cnts, _ = cv.findContours(
        red_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    area = 0
    x = 0
    y = 0
    h = 0
    if len(cnts):
        for c in cnts:
            a = cv.contourArea(c)
            if a > area:
                area = a
                m = cv.moments(c)
                x = m['m10']/m['m00']
                y = m['m01']/m['m00']
        if x != 0 and y != 0:
            h = calculate_height(y)
    return h

def image_processing(frame, umbral_binary):
    _, _, img = cv.split(frame)
    
    ret, img = cv.threshold(img, umbral_binary, 255, cv.THRESH_BINARY)
    img = cv.GaussianBlur(img, (1, 1), 0)
    kernel = np.ones((3, 3), np.uint8)
    img = cv.dilate(img, kernel, iterations=1)
    img = cv.erode(img, kernel, iterations=1)
    img[:200, :] = 0
    return img


def tecnica_rojos(frame, reds):
    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    maskRed1 = cv.inRange(frameHSV, reds[0], reds[1])
    maskRed2 = cv.inRange(frameHSV, reds[2], reds[3])
    maskRed = cv.add(maskRed1, maskRed2)

    return maskRed


def skeleton_media(img, frame):
    skeleton = medial_axis(img)
    skeleton = skeleton.astype(np.uint8) * 255
    # frame = frame.astype(np.uint8) * 255
    frame[skeleton == 255] = [0, 255, 0]
    return frame


def find_centroid(frame):
    red_image = red_technique(frame)
    cnts, _ = cv.findContours(
        red_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    print("No contornos: ", len(cnts))
    area = 0
    x = 0
    y = 0
    if len(cnts) == 0:
        raise ValueError("No se encontraron contornos")

    for c in cnts:
        a = cv.contourArea(c)
        if a > area:
            area = a
            m = cv.moments(c)
            x = m['m10']/m['m00']
            y = m['m01']/m['m00']
    print('x=', x, 'y=', y)

    if x == 0 and y == 0:
        raise ValueError("No se encontro ningun centro")

    distance = calculate_height(y)

    return distance, red_image


def find_middle_pixels(frame, umbral_binary, x, yzero):
    img = image_processing(frame, umbral_binary)
    name = "imgtest/img_erode" + str(x) + ".jpg"
    cv.imwrite(name, img)
    alto, ancho = img.shape
    pixeles_medios = [None] * (ancho)
    # pixeles_medios = np.zeros((ancho,2))
    pix = [0, 0]
    for col in range(ancho):
        columna = img[:, col]
        max = np.argmax(columna)
        min = alto - 1 - np.argmax(np.flip(columna))
        if max > 0 and min > 0:
            if max < 200:
                pix = [col, int((min + min) / 2)]
            else:
                pix = [col, int((max + min) / 2)]
            pixeles_medios[col] = pix
        else:
            pixeles_medios[col] = [col, int(yzero[col])]

    img = np.zeros((img.shape),dtype = np.uint8)
    img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
   
    for pixel in pixeles_medios :
       if pixel is not None:
           img[pixel[1], pixel[0]] = 255
    
    name = "imgtest/img_" + str(x) + ".jpg"
    cv.imwrite(name, img)

    return pixeles_medios


def get_zero(frame, umbral_binary):
    gris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    luminancia_media = cv.mean(gris)[0]
    print("Luminancia media de la imagen:", luminancia_media)
    img = image_processing(frame, umbral_binary)
    #img[:200, :] = 0
    alto, ancho = img.shape
    pixeles_medios = []
    # pixeles_medios = np.zeros((ancho,2))
    pix = [0, 0]
    for col in range(ancho):
        columna = img[:, col]
        max = np.argmax(columna)
        min = alto - np.argmax(np.flip(columna))
        if max > 200 and min > 0:
            if max < 200:
                pix = [col, int((min + min) / 2)]
            else:
                pix = [col, int((max + min) / 2)]
            pixeles_medios.append(pix)

    m = np.array(pixeles_medios)
    mx = m[:, 0]
    my = m[:, 1]
    f = interpolate.interp1d(mx, my, fill_value="extrapolate")
    alto, ancho, _ = frame.shape
    xnew = np.arange(0, ancho, 1)
    ynew = f(xnew)
    #print(ynew)
    #plt.plot(mx, my, 'o', xnew, ynew, '-')
    #plt.show()
    print("ynew size: ",ynew.shape)

    d_zero = calculate_height(ynew[800])

    return d_zero, ynew
