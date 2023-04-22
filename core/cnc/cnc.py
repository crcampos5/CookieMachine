import serial.tools.list_ports
import time
from core.observer import Observer
from core.subject import Subject
from typing import List
import threading

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
        #self.status = threading.Thread(target=self.wait_idle)

    #agrega un objeto observador a la lista de observadores
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    #remueve un objeto observador de la lista de observadores
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    # itera a través de la lista de observadores _observers y llama al 
    # método update() de cada observador, pasándole la instancia actual 
    # de la clase Cnc como argumento
    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    #busca el puerto serial disponible para la conexión
    def find_port(self):
        serial_list = serial.tools.list_ports.comports(include_links=False)
        for i in serial_list:
            self.port = i.device
            
        
    #establece la conexión serial con la máquina CNC
    def connect_serial(self):
        if self.isconect == False :
            self.conection = serial.Serial(self.port, baudrate = 115200, timeout = 2)
            self.msg.insert("Conectado a la maquina")
            self._send("G10 P1 L20 X0 Y0 Z0")
            self.wait_idle()
            self.isconect = True
        else :
            self.conection.close()
        #time.sleep(0.1)

    #envía la señal de "home" a la máquina CNC para mover sus ejes a las coordenadas de origen    
    def home(self):
        #estado = self._send("$G")
        code = "$H"
        data = self._send(code)
        print("Home: ", data)
        self.msg.insert("Haciendo Home")
        self.wait_idle()
        self.ishome = True

    #mueve un eje de la máquina CNC a una posición específica    
    def move(self,axis,value):
        self.wait_idle()
        code = "$J=G21G91"+axis+str(value)+"F"+str(self.pos.F)
        #code = "G10P1L20X0Y0Z0\nG1X1F100"
        #self._send("G10 P1 L20 X0 Y0 Z0")
        print(code)
        data = self._send(code)
        print("data",data)
        self.wait_idle()

    #mueve la máquina CNC a una posición en el plano X-Y
    def movexy(self,x,y):
        x = str(x)
        y = str(y)
        code = "G0G90 X"+ x + " Y" + y
        data = self._send(code)
        self.wait_idle()

    #desbloquea la máquina CNC en caso de que esté en estado de alarma
    def disable_alarm(self):
        self.msg.insert("Desbloqueando...")
        self._send("$X")
        self.wait_idle()
        self.msg.insert("Maquina desbloqueada")

    #espera a que la máquina CNC esté en estado de reposo antes de continuar con el siguiente comando
    def wait_idle(self):
        sigo = True
        while sigo:
            time.sleep(0.1)
            state = self._send("?")
            #print('[INFO] State: ', state)
            sigo = self.process_out(state)
    
    #envía una lista de comandos Gcode a la máquina CNC para ser ejecutados 
    def ejecutar_gcode(self,gcode):
        #self.status.start()
        number_line = 0
        if len(gcode) == 0:
            print("No hay lineas a ejecutar")
        for line in gcode:
            number_line += 1
            code = line.get_string()
            print(code)
            out = self._send(code)
            if out == "ALARM":
                self.msg.insert(out)
                self.notify()
                break
            if number_line % 10 == 0:
                state = self._send("?")
                print('[INFO] State: ', state)
                sigo = self.process_out(state)
           


    def _send(self,code):
        str_send = (code +"\n").encode()
        self.conection.write(str_send)
        #time.sleep(0.001)
        data = self.conection.readline().decode('ascii')
        self.conection.reset_input_buffer()
        return data

    def process_out(self,data):
        if len(data)>1 : #  and "<" in data:
            print('[INFO] State: ', data)
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
                                
                if "Idle" in data:
                    return False
                else: return True
            #elif "ok" in data: return False
            else: return True
        else: False

    # activa o desactiva el láser de la máquina CNC
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
        

