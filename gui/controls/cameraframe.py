import tkinter as tk
from core.sensors.camerasensor import CameraSensor
from gui.componentframe import ComponentFrame

class CameraFrame(ComponentFrame):
    def __init__(self,parent,camera_sensor = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.camera_sensor = camera_sensor
        self.check_camera = tk.IntVar()
        self.check_camera.set(0)
        self.check_quadrant = tk.IntVar()
        self.check_quadrant.set(0)

        self.cbx_show = tk.Checkbutton(self, text="Show Camera",bg='gray90',command=self.show_camera,variable=self.check_camera)
        self.cbx_quadrant = tk.Checkbutton(self, text="S Quadrant",bg='gray90',command=self.search_quadrant,variable=self.check_quadrant)

       # btn_laser = tk.Button(self,text='LASER',font=("Verdana", 12,'bold'),width=8)
        btn_capture = tk.Button(self,text='CAPTURE',font=("Verdana", 12,'bold'),width=8,command=self.capture)

        self.cbx_show.grid(row=0,column=0,padx=5,pady=10)
        self.cbx_quadrant.grid(row=1,column=0,padx=5)
       # btn_laser.grid(row=1,column=0)
        btn_capture.grid(row=2,column=0)

       

        self.grid_propagate(0)
        self.config(width=120,height=180,bg='gray90')

    def set_camera_sensor(self, cs: CameraSensor):
        self.camera_sensor = cs

    def show_camera(self):

        if self.check_camera.get() :
            self.camera_sensor.video()
        else: self.camera_sensor.exit_video()

    def capture(self):
        self.camera_sensor.capture()

    def search_quadrant(self):
        if self.check_quadrant.get() :
            self.camera_sensor.search_quadrant()
        else: self.camera_sensor.exit_quadrant()

    
        