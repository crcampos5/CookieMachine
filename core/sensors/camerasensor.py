import cv2 as cv

class CameraSensor:
    def __init__(self,imagen) -> None:
        self.imagen = imagen
        self.cap = cv.VideoCapture(0,cv.CAP_DSHOW)
        self.exitcap = False

    def video(self):
        print('video camera')
        self.imagen.ban_stopvideo = False
        self.imagen.video(self.cap)

    def exit_video(self):
        self.imagen.ban_stopvideo = True

    def isOpen(self):
        return self.cap.isOpened()

    def capture(self):
        self.imagen.cargar()