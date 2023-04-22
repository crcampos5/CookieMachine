import cv2 as cv
import threading

class LaserSensor(threading.Thread):
    def __init__(self,imagen):
        threading.Thread.__init__(self)
        self.imagen = imagen    
        #self.cap = None #cv.VideoCapture(1)
        self.exitcap = False

    def run(self):
        self.cap = cv.VideoCapture(2)
        print("Resolution w: ",self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        print("Resolution h: ",self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    def video(self):
        print('video laser')
        self.imagen.ban_stopvideo = False
        self.imagen.video(self.cap)

    def exit_video(self):
        self.imagen.ban_stopvideo = True

    def calculate_height(self):
        pass

    def isOpen(self):
        return self.cap.isOpened()

    def opencap(self):
        self.cap.open(2,cv.CAP_MSMF)

    def closecap(self):
        self.cap.release()


    

        
            
        
        