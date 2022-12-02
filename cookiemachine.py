from distutils.log import info
import tkinter as tk
from turtle import bgcolor
from core.cnc.cnc import Cnc
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
from core.sensors.camerasensor import CameraSensor
from core.sensors.lasersensor import LaserSensor


class MainWindow:
    def __init__(self,root):
        self.root = root
        self.root.title('Cookie Machine')
        self.define_geometry()
        self.define_widgets()

        self.imagen1 = Imagen()
        self.imagen2 = Imagen()
        self.camera_sensor = CameraSensor(self.imagen1)
        self.laser_sensor = LaserSensor(self.imagen2)
        
        self.msg = Message()
        self.position = Position(self.root)
        self.cnc = Cnc(self.msg,self.position)        
        self.cnc.attach(self.topbar_frame)

        self.topbar_frame.set_cnc(self.cnc)
        self.images_frame.set_displays(self.imagen1,self.imagen2)
        self.info_frame.set_msg(self.msg)
        self.info_frame.set_pos(self.position)
        self.move_frame.set_cnc(self.cnc)
        self.valve_frame.set_cnc(self.cnc)
        self.laser_frame.set_laser_sensor(self.laser_sensor)
        self.laser_frame.set_cnc(self.cnc)
        self.camera_frame.set_camera_sensor(self.camera_sensor)
        self.cnc.notify()

    

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

    def define_widgets(self):
        self.topbar_frame = TopBarFrame(self.root)
        self.images_frame = ImagesFrame(self.root)
        self.info_frame = InfoFrame(self.root)
        self.controls_frame = tk.Frame(self.root)
        self.runstop_frame = RunStopFrame(self.controls_frame)
        self.move_frame = MoveFrame(self.controls_frame)
        self.speed_frame = SpeedFrame(self.controls_frame)
        self.valve_frame = ValveFrame(self.controls_frame)
        self.laser_frame = LaserFrame(self.controls_frame)
        self.camera_frame = CameraFrame(self.controls_frame)


        self.topbar_frame.grid(row=0,column=0,columnspan=2)
        self.images_frame.grid(row=1,column=0)
        self.info_frame.grid(row=1,column=1,sticky=tk.W)
        self.controls_frame.grid(row=2,column=0,sticky=tk.W)
        self.runstop_frame.grid(row=0,column=0,padx=5)
        self.move_frame.grid(row=0,column=1)
        self.speed_frame.grid(row=0,column=2,padx=5)
        self.valve_frame.grid(row=0,column=3)
        self.laser_frame.grid(row=0,column=4,padx=5)
        self.camera_frame.grid(row=0,column=5)

 
app = tk.Tk()
window = MainWindow(app)
app.mainloop()