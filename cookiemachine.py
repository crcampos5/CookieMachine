from distutils.log import info
import tkinter as tk
from turtle import bgcolor
from cnc.cnc import Cnc
from gui.controls.cameraframe import CameraFrame
from gui.controls.laserframe import LaserFrame
from gui.controls.valveframe import ValveFrame
from gui.controls.moveframe import MoveFrame
from gui.controls.runstopframe import RunStopFrame
from gui.controls.speedframe import SpeedFrame
from gui.imagesframe import ImagesFrame
from gui.topbarframe import TopBarFrame
from gui.infoframe import InfoFrame
from models.imagen import Imagen
from models.message import Message
from models.position import Position
from sensors.camerasensor import CameraSensor
from sensors.lasersensor import LaserSensor


class MainWindow:
    def __init__(self,root):
        self.root = root
        self.root.title('Cookie Machine')
        self.define_geometry()

        self.imagen1 = Imagen()
        self.imagen2 = Imagen()
        self.camera_sensor = CameraSensor(self.imagen1)
        self.laser_sensor = LaserSensor(self.imagen2)
        
        self.msg = Message()
        self.cnc = Cnc(self.msg)
        self.position = Position()


        # defines the primary frames
        topbar_frame = TopBarFrame(self.root,self.cnc) 
        images_frame = ImagesFrame(self.root,self.imagen1,self.imagen2)
        info_frame = InfoFrame(self.root,self.msg,self.position)
        controls_frame = tk.Frame(self.root)
        runstop_frame = RunStopFrame(controls_frame)
        move_frame = MoveFrame(controls_frame,self.cnc)
        speed_frame = SpeedFrame(controls_frame)
        valve_frame = ValveFrame(controls_frame)
        laser_frame = LaserFrame(controls_frame,self.laser_sensor)
        camera_frame = CameraFrame(controls_frame,self.camera_sensor)

        topbar_frame.grid(row=0,column=0,columnspan=2)

        images_frame.grid(row=1,column=0)

        info_frame.grid(row=1,column=1,sticky=tk.W)

        controls_frame.grid(row=2,column=0,sticky=tk.W)
        runstop_frame.grid(row=0,column=0,padx=5)
        move_frame.grid(row=0,column=1)
        speed_frame.grid(row=0,column=2,padx=5)
        valve_frame.grid(row=0,column=3)
        laser_frame.grid(row=0,column=4,padx=5)
        camera_frame.grid(row=0,column=5)

    

    def define_geometry(self):
        w = 1280 # width for the Tk root
        h = 738 # height for the Tk root

        # get screen width and height
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2) - 20

        # set the dimensions of the screen 
        # and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))


app = tk.Tk()
window = MainWindow(app)
app.mainloop()