#coordina la ejecución de un archivo que contiene un diseño a realizar. 
#Tiene una instancia de CameraSensor, LaserSensor y Cnc, que se usan para 
#capturar imágenes, ejecutar el diseño y enviar el código G al CNC, respectivamente.
#El constructor carga parámetros del archivo parameters.json y almacena los valores 
#de quadrants y laser_distance_inyector en la instancia. Además, define una 
# instancia de Template con el nombre del diseño a ejecutar
import importlib
import json
from core.cnc.cnc import Cnc
from core.scanner import Scanner
from core.sensors.camerasensor import CameraSensor
from core.sensors.lasersensor import LaserSensor
from models.message import Message
from core.template import Template

class Core:
    def __init__(self,cam : CameraSensor,laser : LaserSensor,cnc : Cnc) -> None:
        self.cam = cam
        self.laser = laser
        self.cnc = cnc
        self.file = None
        self.stop_ban = False

        with open('parameters/parameters.json', 'r') as f:
            self.parameters = json.load(f)
            self.quadrants = self.parameters["parameters"]["quadrants"]
            self.laser_distance_inyector =self.parameters["parameters"]["laser_distance_inyector"]
            self.resolution = self.parameters["parameters"]["resolution"]
            self.valor_pixel_to_mm = self.parameters["parameters"]["valor_pixel_to_mm"]
            print(self.quadrants)
            f.close()

    #Esta función run() se encarga de ejecutar el proceso principal de la aplicación.
    #utiliza la ruta del archivo seleccionado para importar la clase correspondiente 
    #y crear una instancia de ella. Luego, crea una instancia de la clase Template, 
    #que se encargará de generar el código G que se enviará a la CNC
    def run(self):
        
        if self._check(): #verifica si se cumplen ciertas condiciones para poder continuar
            self.stop_ban = False
            ruta = self.file.replace("/",".").split(".py")[0]
            selected_module = importlib.import_module(ruta)
            elements = dir(selected_module)
            classes = [elem for elem in elements if isinstance(getattr(selected_module, elem), type)]
            klass = getattr(selected_module, classes[0])
            obj = klass()
            self.template = Template(obj.name)
            self.scanner = Scanner(self.laser,self.cnc)
            for q in self.quadrants:
                #Mueve la CNC a la posición del cuadrante actua
                #[-951.000,-243.000]
                self.cnc.movexy(q[0],q[1],"Camara")
                self.msg.insert("Moviendo camara a:" + str(q))
                #Captura una imagen utilizando la cámara
                self.msg.insert("Capturando imagen")
                ret = self.cam.capture()
                if ret : 
                    img = self.cam.imagen
                #Ejecuta el método execute() de la instancia de la clase importada, pasándole la imagen capturada como argumento
                    ban , mensaje = obj.execute(img)
                    if ban :
                    #Genera el código G a partir de la imagen utilizando la instancia de la clase Template
                        print("Generar gcode")
                        self.template.set_imagen(img)
                        x = self.resolution[0]/2/self.valor_pixel_to_mm + self.laser_distance_inyector[0]
                        y = self.resolution[1]/2/self.valor_pixel_to_mm + self.laser_distance_inyector[1]
                        print("Xmm,Ymm: ", x, y)
                        injection_point = [x, y ]
                        gcode = self.template.generate_gcode(injection_point, self.valor_pixel_to_mm)
                    #Ejecutando laser
                        xcentro,ycentro = img.centro
                        a = -1* xcentro/self.valor_pixel_to_mm + x
                        b = -1* ycentro/self.valor_pixel_to_mm + y
                        gcode = self.scanner.scan_centroid(gcode, [a,b])
                    #Ejecuta el código G generado en la CNC
                        print("Ejecutando gcode")
                        self.cnc.save_gcode(gcode)
                        self.cnc.ejecutar_gcode(gcode)
                        
                    else : self.msg.insert(mensaje)

                else : self.msg.insert("No se pudo capturar la imagen")

    #La función _check() verifica que la máquina está conectada, 
    #hay un archivo seleccionado y la máquina está en home
    def _check(self):
        if self.cnc.isconect :
            if self.file != None:
                if self.cnc.ishome: 
                    return True
                else: 
                    self.msg.insert("La maquina no esta es home")                
                    return False    
            else: 
                self.msg.insert("No hay archivo seleccionado")
                return False
        else: 
            self.msg.insert("La maquina no esta conectada")
            return False
        #Verificar camaras abiertas
        #Verificar Home

    def set_msg(self, msg: Message):
        self.msg = msg


    def pause(self):
        self.cnc.pause()

    def stop(self):
        self.stop_ban = True
        self.cnc.stop()
        