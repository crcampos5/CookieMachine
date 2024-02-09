import tkinter as tk
from core.cnc.cnc import Cnc
from core.sensors.lasersensor import LaserSensor
from gui.componentframe import ComponentFrame
from PIL import Image, ImageTk
import operator
import cv2 as cv

class LaserFrame(ComponentFrame):
    def __init__(self,parent,laser_sensor = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.laser_sensor = laser_sensor
        self.check_laser = tk.IntVar()
        self.check_laser.set(0)
        self.activ_laser = False
        self.check_measure = tk.IntVar()
        self.check_measure.set(0)

        self.img_on = ImageTk.PhotoImage(file= 'asset/on.png')
        self.img_off = ImageTk.PhotoImage(file= 'asset/off.png')

        self.cbx_show = tk.Checkbutton(self, text="Show Laser",bg='gray90',command=self.show_laser,variable=self.check_laser)
        self.cbx_measure = tk.Checkbutton(self, text="Measure Height",bg='gray90',command=self.measure,variable=self.check_measure)

        self.btn_laser = tk.Button(self,text=' LASER',font=("Verdana", 12,'bold'),width=110,image=self.img_off,compound = tk.LEFT, anchor=tk.W ,command=self.activate_laser)
        self.btn_laser.image = self.img_off
        btn_capture = tk.Button(self,text=' CAPTURE',font=("Verdana", 12,'bold'),width=110,image=self.img_off,compound = tk.LEFT,anchor=tk.W)
        btn_capture.image = self.img_off
        btn_calibrate = tk.Button(self,text=' Escanear',font=("Verdana", 12,'bold'),width=110,image=self.img_off,compound = tk.LEFT,anchor=tk.W,command=self.calibrate)
        btn_calibrate.image = self.img_off

        self.cbx_show.grid(row=0,column=0,padx=5,pady=10)
        self.cbx_measure.grid(row=1,column=0,padx=5)
        self.btn_laser.grid(row=2,column=0)
        btn_capture.grid(row=3,column=0,padx=5)
        btn_calibrate.grid(row=5,column=0)

       

        self.grid_propagate(0)
        self.config(width=130,height=180,bg='gray90')
    
    def set_cnc(self, cnc: Cnc):
        self.cnc = cnc
        self.laser_sensor.set_cnc(cnc)

    def set_laser_sensor(self, lsr: LaserSensor):
        self.laser_sensor = lsr

    def show_laser(self):

        if self.check_laser.get() :
            self.laser_sensor.video()
        else: self.laser_sensor.exit_video()

    def measure(self):
        if self.check_measure.get() :
            self.laser_sensor.measure_height()
    
    def activate_laser(self):
        self.activ_laser = operator.not_(self.activ_laser)
        if self.activ_laser :
            self.cnc.laseronoff(True)
            self.btn_laser.config(image = self.img_on)
            self.btn_laser.image = self.img_on
        else:
            self.cnc.laseronoff(False)
            self.btn_laser.config(image = self.img_off)
            self.btn_laser.image = self.img_off
    
    def calibrate(self):
        #self.cnc.move_to_quadrant("Laser")
        self.laser_sensor.scan_line([-931.6,-73.2])

        

    
