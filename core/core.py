import importlib
import json
from core.cnc.cnc import Cnc
from core.sensors.camerasensor import CameraSensor
from core.sensors.lasersensor import LaserSensor

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
            for q in self.quadrants:
                #Mover a cuadrante
                self.cnc.movexy(q[0],q[1])
                #Capturar foto
                ret = self.cam.capture()
                if ret : img = self.cam.imagen
                #Ejecutar disenio
                obj.execute(img)
                #Generar gcode

                #Ejecutar gcode

    def _check(self):
        if self.file != None: return True
        else: 
            print("No hay archivo seleccionado")
            return False
        #Verificar camaras abiertas
        #Verificar Home
        