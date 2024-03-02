import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from core.parametros import Parametros
import numpy as np

from core.sensors.lasersensor import LaserSensor

#Clase padre de los frame 
class ConfigLaserWindow(tk.Toplevel):

    def __init__(self,parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title("Config Laser")
        self.geometry("640x480")

        self.parametros = Parametros()
        self.laser_sensor = LaserSensor()

        #variables de estado ---------
        self.video_is_on = False
        self.laser = False
        self.pwer_laser = tk.IntVar()

        self.expositure = tk.IntVar()
        self.binary_ban = tk.BooleanVar()
        self.binary_ban.set(False)
        self.media_ban = tk.BooleanVar()
        self.media_ban.set(False)
        self.umbral_binary = tk.IntVar()
        self.umbral_binary.set(127)

        self.a_h_1 = tk.IntVar()
        self.a_h_2 = tk.IntVar()
        self.a_s_1 = tk.IntVar()
        self.a_s_2 = tk.IntVar()
        self.a_v_1 = tk.IntVar()
        self.a_v_2 = tk.IntVar()

        self.b_h_1 = tk.IntVar()
        self.b_h_2 = tk.IntVar()
        self.b_s_1 = tk.IntVar()
        self.b_s_2 = tk.IntVar()
        self.b_v_1 = tk.IntVar()
        self.b_v_2 = tk.IntVar()

        self.a_h_1.set(0)
        self.a_h_2.set(16)
        self.a_s_1.set(0)
        self.a_s_2.set(255)
        self.a_v_1.set(53)
        self.a_v_2.set(255)

        self.b_h_1.set(160)
        self.b_h_2.set(179)
        self.b_s_1.set(0)
        self.b_s_2.set(255)
        self.b_v_1.set(37)
        self.b_v_2.set(255)
        
        #-----------------------------
        self.pwer_laser.set(self.parametros.get_parametro("laser_intensity"))
        self.expositure.set(self.parametros.get_parametro("expositure"))

        #img = ImageTk.PhotoImage(file= 'asset/noimage500x500.jpg')
        #lbl_imagen = ttk.Label(self,image=img)                                                                                                                                                  
        #lbl_imagen.image = img
        self.btn_mostrar_video = ttk.Button(self,text = "Iniciar Video", command=self.video_on)
        self.btn_encender_laser = ttk.Button(self,text = "Iniciar Laser", command=self.laser_on)
        self.scl_pwer_laser = ttk.Scale(self, orient="horizontal", length=200, from_=0, to=500 ,variable=self.pwer_laser,command=self.set_power_laser)
        self.lbl_pwer_laser = ttk.Label(self,text="Intensidad del Laser: ")
        self.lbl_pwer_laser["text"] = "Intensidad del Laser: " + str(self.pwer_laser.get())

        lbf_param_cam = ttk.Labelframe(self, text='Parametros de camara')
        self.lbl_expositure = ttk.Label(lbf_param_cam,text="Exposicion: ")
        self.scl_expositure = ttk.Scale(lbf_param_cam, orient="horizontal", length=200, from_=-13, to=-1 ,variable=self.expositure,command=self.set_expositure)
        self.lbl_var_expositure = ttk.Label(lbf_param_cam,text="")

        


        #lbl_imagen.grid(row=0,column=0,rowspan=4,padx=5)
        self.btn_mostrar_video.grid(row=0,column=0,sticky='n')  
        self.btn_encender_laser.grid(row=1,column=0,sticky='n')
        self.lbl_pwer_laser.grid(row=2,column=0,sticky='n')
        self.scl_pwer_laser.grid(row=2,column=1,sticky='n')

        lbf_param_cam.grid(row=3,column=0,columnspan=2,sticky='new',padx=5)
        self.lbl_expositure.grid(row=0,column=0,sticky='n')
        self.scl_expositure.grid(row=0,column=1,sticky='n')
        self.lbl_var_expositure.grid(row=0,column=3,sticky='n')

        #---------------------------------------------Rojos
        

        #--------------------------------------------------
        self.create_widgets()
        
        self.set_rojos(None)

    def video_on(self):
        self.video_is_on = not self.video_is_on
        if self.video_is_on :
            self.laser_sensor.video()
            self.btn_mostrar_video["text"] = "Parar Video"                                                                                                                                                                                               
        else :  
            self.laser_sensor.stop_video()
            self.btn_mostrar_video["text"] = "Iniciar Video"

    def laser_on(self):
        self.laser = not self.laser
        if self.laser :
            self.parent.activate_laser()
            self.btn_encender_laser["text"] = "Parar Laser"
        else : 
            self.parent.activate_laser() 
            self.btn_encender_laser["text"] = "Iniciar Laser"

    def set_power_laser(self,e):
        self.parent.laser_power.set(int(self.pwer_laser.get()))
        self.lbl_pwer_laser["text"] = "Intensidad del Laser: " + str(int(self.pwer_laser.get()))
        self.parent.set_laserpower(e)

    def set_expositure(self,e):
        self.lbl_var_expositure["text"] = str(self.expositure.get())
         
    def set_rojos(self,e):
        self.lbl_var_a_h_1["text"] = str(self.a_h_1.get())
        self.lbl_var_a_h_2["text"] = str(self.a_h_2.get())
        self.lbl_var_a_s_1["text"] = str(self.a_s_1.get())
        self.lbl_var_a_s_2["text"] = str(self.a_s_2.get())
        self.lbl_var_a_v_1["text"] = str(self.a_v_1.get())
        self.lbl_var_a_v_2["text"] = str(self.a_v_2.get())
        self.lbl_var_b_h_1["text"] = str(self.b_h_1.get())
        self.lbl_var_b_h_2["text"] = str(self.b_h_2.get())
        self.lbl_var_b_s_1["text"] = str(self.b_s_1.get())
        self.lbl_var_b_s_2["text"] = str(self.b_s_2.get())
        self.lbl_var_b_v_1["text"] = str(self.b_v_1.get())
        self.lbl_var_b_v_2["text"] = str(self.b_v_2.get())

        redBajo1 = np.array([self.a_h_1.get(), self.a_s_1.get(), self.a_v_1.get()], np.uint8)
        redAlto1 = np.array([self.a_h_2.get(), self.a_s_2.get(), self.a_v_2.get()], np.uint8)
        redBajo2=np.array([self.b_h_1.get(), self.b_s_1.get(), self.b_v_1.get()], np.uint8)
        redAlto2=np.array([self.b_h_2.get(), self.b_s_2.get(), self.b_v_2.get()], np.uint8)

        self.laser_sensor.redBajo1 = redBajo1 
        self.laser_sensor.redAlto1 = redAlto1
        self.laser_sensor.redBajo2 = redBajo2
        self.laser_sensor.redAlto2 = redAlto2
        

    def process(self,e):
        pass

    def activate_binary(self,e = None):
        self.lbl_umbral_binary["text"] = str(int(self.umbral_binary.get()))
        self.laser_sensor.binary_ban = self.binary_ban.get()
        self.laser_sensor.umbral_binary = self.umbral_binary.get()

    def activate_media(self):
        self.laser_sensor.linea_media_ban = self.media_ban.get()

    def get_focus(self):
        f = self.laser_sensor.get_focus()
        self.lbl_focus["text"] = str(f)


    def create_widgets(self):

        check_binary = ttk.Checkbutton(self, text='Binary', command=self.activate_binary, variable=self.binary_ban)
        check_binary.grid(row=0,column=3,sticky='new',padx=5)

        scl_umbral_binary = ttk.Scale(self, orient="horizontal", length=200, from_=0, to=179 ,variable=self.umbral_binary,command=self.activate_binary)
        scl_umbral_binary.grid(row=0,column=4,sticky='new')

        self.lbl_umbral_binary = ttk.Label(self,text="")
        self.lbl_umbral_binary.grid(row=0,column=5,sticky='new')

        check_media = ttk.Checkbutton(self, text='Linea Media', command=self.activate_media, variable=self.media_ban)
        check_media.grid(row=1,column=3,sticky='new',padx=5)

        self.btn_get_focus = ttk.Button(self,text = "Obtener Focus", command=self.get_focus)
        self.btn_get_focus.grid(row=2,column=3,sticky='new')

        self.lbl_focus = ttk.Label(self,text="")
        self.lbl_focus.grid(row=2,column=4,sticky='new')

        lbf_param_rojos_a = ttk.Labelframe(self, text='Parametros de Rojos A')
        self.lbl_a_h_1 = ttk.Label(lbf_param_rojos_a,text="H Bajo: ")
        self.scl_a_h_1 = ttk.Scale(lbf_param_rojos_a, orient="horizontal", length=200, from_=0, to=179 ,variable=self.a_h_1,command=self.set_rojos)
        self.lbl_var_a_h_1 = ttk.Label(lbf_param_rojos_a,text="")

        self.lbl_a_h_2 = ttk.Label(lbf_param_rojos_a,text="H Alto: ")
        self.scl_a_h_2 = ttk.Scale(lbf_param_rojos_a, orient="horizontal", length=200, from_=0, to=179 ,variable=self.a_h_2,command=self.set_rojos)
        self.lbl_var_a_h_2 = ttk.Label(lbf_param_rojos_a,text="")

        self.lbl_a_s_1 = ttk.Label(lbf_param_rojos_a,text="S Bajo: ")
        self.scl_a_s_1 = ttk.Scale(lbf_param_rojos_a, orient="horizontal", length=200, from_=0, to=255 ,variable=self.a_s_1,command=self.set_rojos)
        self.lbl_var_a_s_1 = ttk.Label(lbf_param_rojos_a,text="")

        self.lbl_a_s_2 = ttk.Label(lbf_param_rojos_a,text="S Alto: ")
        self.scl_a_s_2 = ttk.Scale(lbf_param_rojos_a, orient="horizontal", length=200, from_=0, to=255 ,variable=self.a_s_2,command=self.set_rojos)
        self.lbl_var_a_s_2 = ttk.Label(lbf_param_rojos_a,text="")

        self.lbl_a_v_1 = ttk.Label(lbf_param_rojos_a,text="V Bajo: ")
        self.scl_a_v_1 = ttk.Scale(lbf_param_rojos_a, orient="horizontal", length=200, from_=0, to=255 ,variable=self.a_v_1,command=self.set_rojos)
        self.lbl_var_a_v_1 = ttk.Label(lbf_param_rojos_a,text="")

        self.lbl_a_v_2 = ttk.Label(lbf_param_rojos_a,text="V Alto: ")
        self.scl_a_v_2 = ttk.Scale(lbf_param_rojos_a, orient="horizontal", length=200, from_=0, to=255 ,variable=self.a_v_2,command=self.set_rojos)
        self.lbl_var_a_v_2 = ttk.Label(lbf_param_rojos_a,text="")

        lbf_param_rojos_a.grid(row=4,column=0,columnspan=2,sticky='new',padx=5)
        self.lbl_a_h_1.grid(row=0,column=0,sticky='n')
        self.scl_a_h_1.grid(row=0,column=1,sticky='n')
        self.lbl_var_a_h_1.grid(row=0,column=3,sticky='n')

        self.lbl_a_h_2.grid(row=1,column=0,sticky='n')
        self.scl_a_h_2.grid(row=1,column=1,sticky='n')
        self.lbl_var_a_h_2.grid(row=1,column=3,sticky='n')

        self.lbl_a_s_1.grid(row=2,column=0,sticky='n')
        self.scl_a_s_1.grid(row=2,column=1,sticky='n')
        self.lbl_var_a_s_1.grid(row=2,column=3,sticky='n')

        self.lbl_a_s_2.grid(row=3,column=0,sticky='n')
        self.scl_a_s_2.grid(row=3,column=1,sticky='n')
        self.lbl_var_a_s_2.grid(row=3,column=3,sticky='n')

        self.lbl_a_v_1.grid(row=4,column=0,sticky='n')
        self.scl_a_v_1.grid(row=4,column=1,sticky='n')
        self.lbl_var_a_v_1.grid(row=4,column=3,sticky='n')

        self.lbl_a_v_2.grid(row=5,column=0,sticky='n')
        self.scl_a_v_2.grid(row=5,column=1,sticky='n')
        self.lbl_var_a_v_2.grid(row=5,column=3,sticky='n')

        lbf_param_rojos_b = ttk.Labelframe(self, text='Parametros de Rojos B')
        self.lbl_b_h_1 = ttk.Label(lbf_param_rojos_b,text="H Bajo: ")
        self.scl_b_h_1 = ttk.Scale(lbf_param_rojos_b, orient="horizontal", length=200, from_=0, to=179 ,variable=self.b_h_1,command=self.set_rojos)
        self.lbl_var_b_h_1 = ttk.Label(lbf_param_rojos_b,text="")

        self.lbl_b_h_2 = ttk.Label(lbf_param_rojos_b,text="H Alto: ")
        self.scl_b_h_2 = ttk.Scale(lbf_param_rojos_b, orient="horizontal", length=200, from_=0, to=179 ,variable=self.b_h_2,command=self.set_rojos)
        self.lbl_var_b_h_2 = ttk.Label(lbf_param_rojos_b,text="")

        self.lbl_b_s_1 = ttk.Label(lbf_param_rojos_b,text="S Bajo: ")
        self.scl_b_s_1 = ttk.Scale(lbf_param_rojos_b, orient="horizontal", length=200, from_=0, to=255 ,variable=self.b_s_1,command=self.set_rojos)
        self.lbl_var_b_s_1 = ttk.Label(lbf_param_rojos_b,text="")

        self.lbl_b_s_2 = ttk.Label(lbf_param_rojos_b,text="S Alto: ")
        self.scl_b_s_2 = ttk.Scale(lbf_param_rojos_b, orient="horizontal", length=200, from_=0, to=255 ,variable=self.b_s_2,command=self.set_rojos)
        self.lbl_var_b_s_2 = ttk.Label(lbf_param_rojos_b,text="")

        self.lbl_b_v_1 = ttk.Label(lbf_param_rojos_b,text="V Bajo: ")
        self.scl_b_v_1 = ttk.Scale(lbf_param_rojos_b, orient="horizontal", length=200, from_=0, to=255 ,variable=self.b_v_1,command=self.set_rojos)
        self.lbl_var_b_v_1 = ttk.Label(lbf_param_rojos_b,text="")

        self.lbl_b_v_2 = ttk.Label(lbf_param_rojos_b,text="V Alto: ")
        self.scl_b_v_2 = ttk.Scale(lbf_param_rojos_b, orient="horizontal", length=200, from_=0, to=255 ,variable=self.b_v_2,command=self.set_rojos)
        self.lbl_var_b_v_2 = ttk.Label(lbf_param_rojos_b,text="")

        lbf_param_rojos_b.grid(row=5,column=0,columnspan=2,sticky='new',padx=5)
        self.lbl_b_h_1.grid(row=0,column=0,sticky='n')
        self.scl_b_h_1.grid(row=0,column=1,sticky='n')
        self.lbl_var_b_h_1.grid(row=0,column=3,sticky='n')

        self.lbl_b_h_2.grid(row=1,column=0,sticky='n')
        self.scl_b_h_2.grid(row=1,column=1,sticky='n')
        self.lbl_var_b_h_2.grid(row=1,column=3,sticky='n')

        self.lbl_b_s_1.grid(row=2,column=0,sticky='n')
        self.scl_b_s_1.grid(row=2,column=1,sticky='n')
        self.lbl_var_b_s_1.grid(row=2,column=3,sticky='n')

        self.lbl_b_s_2.grid(row=3,column=0,sticky='n')
        self.scl_b_s_2.grid(row=3,column=1,sticky='n')
        self.lbl_var_b_s_2.grid(row=3,column=3,sticky='n')

        self.lbl_b_v_1.grid(row=4,column=0,sticky='n')
        self.scl_b_v_1.grid(row=4,column=1,sticky='n')
        self.lbl_var_b_v_1.grid(row=4,column=3,sticky='n')

        self.lbl_b_v_2.grid(row=5,column=0,sticky='n')
        self.scl_b_v_2.grid(row=5,column=1,sticky='n')
        self.lbl_var_b_v_2.grid(row=5,column=3,sticky='n')
