
from core.cnc.cnc import Cnc
from core.sensors.lasersensor import LaserSensor


class Scanner:

    def __init__(self, laser : LaserSensor , cnc : Cnc) -> None:
        self.laser = laser
        self.cnc = cnc
        self.laser_cero = 170.99
        self.z_travel = -56

    def scan_centroid(self, gcode, centroide ):
        print("Centroide: ", centroide )
        self.cnc.movexy(centroide[0],centroide[1],"Laser")
        self.laser.measure_height()
        h = self.laser_cero - self.laser.distance
        print("Altura: ", h)
        z = self.z_travel + h + 0.5
        print("Altura de z: ",z)

        self._process_gcode(z,gcode)
        return gcode

        

    def scan_points(self):
        pass

    def scan_line(self):
        pass

    def _process_gcode(self,altura,gcode):
        z_seguro = altura + 5
        for line in gcode:
            z = line.get_z()
            if(z != None):
                if z == 5 : 
                    z = z_seguro
                else: z = altura
                line.set_z(z)