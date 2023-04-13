import serial.tools.list_ports
import time
from core.observer import Observer
from core.subject import Subject
from typing import List

from models.message import Message

#<Run|MPos:135.632,0.000,0.000|FS:100,0>
#<Idle|MPos:0.000,0.000,0.000|FS:0,0>
#<Alarm|MPos:0.000,0.000,0.000|FS:0,0|WCO:120.000,140.000,-5.000>

class Cnc(Subject):
    def __init__(self,msg = None,pos = None) -> None:

        self._observers: List[Observer] = []
        self.msg = msg
        self.pos = pos
        self.port = None
        self.alarm = False
        self.ishome = False
        self.isconect = False
        self.find_port()

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)


    def find_port(self):
        serial_list = serial.tools.list_ports.comports(include_links=False)
        for i in serial_list:
            self.port = i.device
            
        

    def connect_serial(self):
        self.conection = serial.Serial(self.port, baudrate = 115200, timeout = 2)
        self.msg.insert("Conectado a la maquina")
        self.wait_idle()
        self.isconect = True
        #time.sleep(0.1)

    def home(self):
        code = "$H"
        data = self._send(code)
        self.msg.insert("Haciendo Home")
        print("data",data)
        self.wait_idle()
        self.ishome = True

    def move(self,axis,value):
        code = "$J=G21G91"+axis+str(value)+"F"+str(self.pos.F)
        #code = "G10P1L20X0Y0Z0\nG1X1F100"
        print(code)
        data = self._send(code)
        print("data",data)
        self.wait_idle()

    def movexy(self,x,y):
        x = str(x)
        y = str(y)

        code = "G0 X"+ x + " Y" + y
        data = self._send(code)
        print("data",data)
        self.wait_idle()

    def disable_alarm(self):
        self.msg.insert("Desbloqueando...")
        self._send("$X")
        self.wait_idle()
        self.msg.insert("Maquina desbloqueada")

    def wait_idle(self):
        sigo = True
        while sigo:
            time.sleep(0.3)
            state = self._send("?")
            print('[INFO] State: ', state)
            sigo = self.process_out(state)
    
    #Esta funcion ejecuta el gcode que se le envie 
    def ejecutar_gcode(self,gcode):

        for line in gcode:
            code = line.get_string()
            print(code)
            self._send(code)
            self.wait_idle()


    def _send(self,code):
        str_send = (code +"\n").encode()
        self.conection.write(str_send)
        #time.sleep(0.001)
        data = self.conection.readline().decode('ascii')
        self.conection.reset_input_buffer()
        return data

    def process_out(self,data):
        if(len(data)>1):
            if "Alarm" in  data:
                a = data.find('WCO')
                if(a != -1):
                    a = a + 4
                    x,y,z = data[a:(a+17)].split(',')
                    self.pos.set_pos(x,y,z)
                self.msg.insert("Maquina bloqueada!")
                self.alarm = True
                self.notify()
            elif "MPos" in data:
                #a = data.split("|")
                a = data.find("MPos") + 5
                b = data.find("F") - 1
                x,y,z = data[a:b].split(',')
                self.pos.set_pos(x,y,z)        
                #print(x,y,z)     
                #for item in a:
                #    if "Mpos" in item:
                #        b = item.split(":")[1]
                #        x,y,z = b.split(',')
                #        self.pos.set_pos(x,y,z)
                #        print(x,y,z)
                #        break
                #a = data.split("|")[1].split(":")[1]
                
                if "Idle" in data:
                    return False
                else: return True
            else: return True
        else: False

    def laseronoff(self, ban: bool):
        if ban :
            self.msg.insert("Activando laser")
            data = self._send("G1 S50 F100")
            print(data)
            data = self._send("M3")
        else :
            data = self._send("M5")
            self.msg.insert("Desactivando laser")
            print(data)
        

