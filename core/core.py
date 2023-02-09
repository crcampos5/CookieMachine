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
            print(self.quadrants)
        
    def run(self):
        if self._check():
            ruta = self.file.replace("/",".").split(".py")[0]
            selected_module = importlib.import_module(ruta)
            elements = dir(selected_module)
            classes = [elem for elem in elements if isinstance(getattr(selected_module, elem), type)]
            klass = getattr(selected_module, classes[0])
            obj = klass()
            self.template = Template(obj.name)
            for q in self.quadrants:
                #Mover a cuadrante
                self.cnc.movexy(q[0],q[1])
                self.msg.insert("Moviendo maquina a:" + str(q))
                #Capturar foto
                self.msg.insert("Capturando imagen")
                ret = self.cam.capture()
                if ret : 
                    img = self.cam.imagen
                #Ejecutar disenio
                    obj.execute(img)
                #Generar gcode
                    self.template.set_imagen(img)
                #Ejecutar gcode
                else : self.msg.insert("No se pudo capturar la imagen")

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
        