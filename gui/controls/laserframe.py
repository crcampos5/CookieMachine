import tkinter as tk
from tkinter import ttk
from core.cnc.cnc import Cnc
from core.observer import Observer
from core.parametros import Parametros
from core.sensors.lasersensor import LaserSensor
from core.subject import Subject
from gui.componentframe import ComponentFrame
from PIL import Image, ImageTk
import operator
import cv2 as cv
from gui.windows.config_laser_window import ConfigLaserWindow

class LaserFrame(ComponentFrame,Observer):
    def __init__(self,parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.parameters = Parametros()
        self.laser_sensor = LaserSensor()
        #self.check_laser = tk.IntVar()
        #self.check_laser.set(0)
        self.activ_laser = False
        self.check_open_config = tk.BooleanVar()
        self.check_open_config.set(False)
        self.laser_power = tk.IntVar()
        p = self.parameters.get_parametro("laser_intensity")
        self.laser_power.set(p)

        self.img_on = ImageTk.PhotoImage(file= 'asset/on.png')
        self.img_off = ImageTk.PhotoImage(file= 'asset/off.png')

        self.btn_show = ttk.Button(self, text="Mostrar Laser",command=self.show_laser)
        self.cbx_config = ttk.Checkbutton(self, text="Config",command=self._open_config,variable=self.check_open_config)

        self.btn_measure = ttk.Button(self,text=' Medir Altura',image=self.img_off,compound = tk.LEFT,command=self.measure)
        self.btn_measure.image = self.img_off
        self.btn_laser = tk.Button(self,text=' LASER',font=("Verdana", 12,'bold'),width=110,image=self.img_off,compound = tk.LEFT, anchor=tk.W ,command=self.activate_laser)
        self.btn_laser.image = self.img_off
        btn_capture = tk.Button(self,text=' CAPTURE',font=("Verdana", 12,'bold'),width=110,image=self.img_off,compound = tk.LEFT,anchor=tk.W,command=self.capture)
        btn_capture.image = self.img_off
        btn_escanear = tk.Button(self,text=' Escanear',font=("Verdana", 12,'bold'),width=110,image=self.img_off,compound = tk.LEFT,anchor=tk.W,command=self.escanear)
        btn_escanear.image = self.img_off
        self.slr_laser_power = ttk.Scale(self,from_=500,to=0,orient='vertical',variable=self.laser_power,length=150,command=self.set_laserpower)

        self.cbx_config.grid(row=0,column=0,padx=5, sticky='w')
        self.btn_show.grid(row=1,column=0,padx=5, sticky='w')
        self.btn_measure.grid(row=2,column=0,padx=5, sticky='w')

        self.btn_laser.grid(row=3,column=0)
        btn_capture.grid(row=4,column=0,padx=5)
        btn_escanear.grid(row=5,column=0)
        self.slr_laser_power.grid(row=0,column=1, rowspan=6, padx=5)

       

        self.grid_propagate(0)
        self.config(width=180,height=180,bg='gray90')
    
    def update(self, subject: Subject) -> None:
        self.activ_laser = subject.laser_on
        if self.activ_laser :
            self.btn_laser.config(image = self.img_on)
            self.btn_laser.image = self.img_on
        else : 
            self.btn_laser.config(image = self.img_off)
            self.btn_laser.image = self.img_off
    
    def set_cnc(self, cnc: Cnc):
        self.cnc = cnc
        self.laser_sensor.set_cnc(cnc)

    def show_laser(self):
        self.laser_sensor.video()

    def measure(self):
        self.laser_sensor.measure_height()
    
    def activate_laser(self):
        self.activ_laser = operator.not_(self.activ_laser)
        if self.activ_laser :
            ret = self.cnc.laser_onoff(True)
            print("Laser activo: ", ret)
            self.btn_laser.config(image = self.img_on)
            self.btn_laser.image = self.img_on
        else:
            self.cnc.laser_onoff(False)
            self.btn_laser.config(image = self.img_off)
            self.btn_laser.image = self.img_off
    
    def escanear(self):
        #self.laser_sensor.scan_line([-931.6,-73.2])
        self.laser_sensor.sweep_scan([-931.6,-73.2])

    def capture(self):
        pass

    def set_laserpower(self,e):
        self.cnc.laserpower(self.laser_power.get())
        #print(self.laser_power.get())
        
    def _open_config(self):
        if self.check_open_config.get() :
            self.config_laser_window = ConfigLaserWindow(self)
            self.config_laser_window.protocol("WM_DELETE_WINDOW", self._close_config)
        else : self._close_config()

    def _close_config(self):
        self.check_open_config.set(False)
        self.config_laser_window.destroy()
        

    
