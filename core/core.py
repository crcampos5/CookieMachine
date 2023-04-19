#coordina la ejecución de un archivo que contiene un diseño a realizar. 
#Tiene una instancia de CameraSensor, LaserSensor y Cnc, que se usan para 
#capturar imágenes, ejecutar el diseño y enviar el código G al CNC, respectivamente.
#El constructor carga parámetros del archivo parameters.json y almacena los valores 
#de quadrants y laser_distance_inyector en la instancia. Además, define una 
# instancia de Template con el nombre del diseño a ejecutar
import importlib
import json
from core.cnc.cnc import Cnc
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

        with open('parameters/parameters.json', 'r') as f:
            self.parameters = json.load(f)
            self.quadrants = self.parameters["parameters"]["quadrants"]
            self.laser_distance_inyector =self.parameters["parameters"]["laser_distance_inyector"]
            print(self.quadrants)

    #Esta función run() se encarga de ejecutar el proceso principal de la aplicación.
    #utiliza la ruta del archivo seleccionado para importar la clase correspondiente 
    #y crear una instancia de ella. Luego, crea una instancia de la clase Template, 
    #que se encargará de generar el código G que se enviará a la CNC
    def run(self):
        
        if self._check(): #verifica si se cumplen ciertas condiciones para poder continuar
            ruta = self.file.replace("/",".").split(".py")[0]
            selected_module = importlib.import_module(ruta)
            elements = dir(selected_module)
            classes = [elem for elem in elements if isinstance(getattr(selected_module, elem), type)]
            klass = getattr(selected_module, classes[0])
            obj = klass()
            self.template = Template(obj.name)
            for q in self.quadrants:
                #Mueve la CNC a la posición del cuadrante actua
                self.cnc.movexy(q[0],q[1])
                self.msg.insert("Moviendo maquina a:" + str(q))
                #Captura una imagen utilizando la cámara
                self.msg.insert("Capturando imagen")
                ret = self.cam.capture()
                if ret : 
                    img = self.cam.imagen
                #Ejecuta el método execute() de la instancia de la clase importada, pasándole la imagen capturada como argumento
                    obj.execute(img)
                #Genera el código G a partir de la imagen utilizando la instancia de la clase Template
                    print("Generar gcode")
                    self.template.set_imagen(img)
                    gcode = self.template.generate_gcode(q)
                #Ejecuta el código G generado en la CNC
                    print("Ejecutando gcode")
                    self.cnc.ejecutar_gcode(gcode)

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
        