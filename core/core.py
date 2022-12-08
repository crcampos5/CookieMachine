import json
from core.cnc.cnc import Cnc
from core.sensors.camerasensor import CameraSensor
from core.sensors.lasersensor import LaserSensor

class Core:
    def __init__(self,cam : CameraSensor,laser : LaserSensor,cnc : Cnc) -> None:
        self.cam = cam
        self.laser = laser
        self.cnc = cnc

        with open('parameters/parameters.json', 'r') as f:
            self.parameters = json.load(f)
            self.quadrants = self.parameters.quadrants
        
    def run(self):
        if self._check():
            for q in self.quadrants:
                self.cnc.movexy(q[0],q[1])
                self.cam.capture()

    def _check(self):
        #Verificar parametros
        #Verificar camaras abiertas
        #Verificar Home
        return True