import cv2 as cv

class LaserSensor:
    def __init__(self,imagen) -> None:
        self.imagen = imagen
        self.cap = cv.VideoCapture(2,cv.CAP_DSHOW)
        self.exitcap = False

    def video(self):
        print('video laser')
        self.imagen.ban_stopvideo = False
        self.imagen.video(self.cap)

    def exit_video(self):
        self.imagen.ban_stopvideo = True

    def isOpen(self):
        return self.cap.isOpened()
               
        
            
        
        