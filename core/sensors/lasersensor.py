import cv2 as cv

class LaserSensor:
    def __init__(self,imagen) -> None:
        self.imagen = imagen
        self.cap = None #cv.VideoCapture()
        self.exitcap = False

    def video(self):
        print('video laser')
        self.imagen.ban_stopvideo = False
        self.imagen.video(self.cap)

    def exit_video(self):
        self.imagen.ban_stopvideo = True

    def isOpen(self):
        return self.cap.isOpened()

    def opencap(self):
        self.cap.open(2,cv.CAP_MSMF)

    def closecap(self):
        self.cap.release()
    
               
        
            
        
        