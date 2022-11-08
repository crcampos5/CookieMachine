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
        #time.sleep(0.1)

    def move(self,axis,value):
        print("mover")
        code = "$J=G21G91"+axis+str(value)+"F100"
        code = "G10P1L20X0Y0Z0\nG1X1F100"
        print(code)
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
            time.sleep(0.1)
            state = self._send("?")
            print('[INFO] Sta: ', state)
            sigo = self.process_out(state)
            #if(len(state)>1):
            #   if state[1] == 'I':
            #        self.msg.insert('[INFO] State: '+state)
            #        break
            #   elif state[1] == 'A':
            #       print("[INFO] Alarm")
            #       self.msg.insert("Maquina bloqueada!")
            #       self.alarm = True
            #       self.notify()
            #       break
            #else: break

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
                a = data.find('WCO') + 3
                x,y,z = data[a:-1].split(',')
                self.pos.set_pos(x,y,z)
                self.msg.insert("Maquina bloqueada!")
                self.alarm = True
                self.notify()
            elif "MPos" in data:
                a = data.find('MPos') + 4
                x,y,z = data[a:-1].split(',')
                self.pos.set_pos(x,y,z)
            else: return True
        else: False

        

