import tkinter as tk
from core.cnc.cnc import Cnc
from core.sensors.camerasensor import CameraSensor
from gui.componentframe import ComponentFrame

class CalibrateFrame(ComponentFrame):
    def __init__(self,parent,camera_sensor = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.camera_sensor = camera_sensor
        self.option = tk.IntVar()

        self.rbt_boquilla = tk.Radiobutton(self, text="Boquilla",bg='gray90',command=self.calibrate,variable=self.option, value=1)
        self.rbt_camara = tk.Radiobutton(self, text="Camara",bg='gray90',command=self.calibrate,variable=self.option, value=2)
        self.rbt_laser = tk.Radiobutton(self, text="Laser",bg='gray90',command=self.calibrate,variable=self.option, value=3)

        btn_calibrar = tk.Button(self,text='CALIBRAR',font=("Verdana", 12,'bold'),width=8,command=self.calibrar)

        self.rbt_boquilla.grid(row=0,column=0,padx=5,pady=10)
        self.rbt_camara.grid(row=1,column=0,padx=5)
        self.rbt_laser.grid(row=2,column=0,padx=5)
        btn_calibrar.grid(row=3,column=0,padx=5)

       

        self.grid_propagate(0)
        self.config(width=120,height=180,bg='gray90')

    def set_camera_sensor(self, cs: CameraSensor):
        self.camera_sensor = cs

    def set_cnc(self, cnc : Cnc):
        self.cnc = cnc

    def show_camera(self):

        if self.check_camera.get() :
            self.camera_sensor.video()
        else: self.camera_sensor.exit_video()

    def calibrate(self):
        option = self.option.get()
        if option == 1:
            self.cnc.move_to_quadrant("Boquilla")
        elif option == 2:
            self.cnc.move_to_quadrant("Camara")
        elif option == 3:
            self.cnc.move_to_quadrant("Laser")


    def calibrar(self):
        pass