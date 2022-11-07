import serial.tools.list_ports
import time

#<Run|MPos:135.632,0.000,0.000|FS:100,0>
#<Idle|MPos:0.000,0.000,0.000|FS:0,0>
#<Alarm|MPos:0.000,0.000,0.000|FS:0,0|WCO:120.000,140.000,-5.000>

class Cnc:
    def __init__(self,msg) -> None:
        self.msg = msg
        self.port = None
        self.alarm = False
        #self.find_port()
       # self.conect_serial()
        #self.wait_idle()

    def find_port(self):
        serial_list = serial.tools.list_ports.comports(include_links=False)
        for i in serial_list:
            self.port = i.device
        return [self.port]

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
        while True:
            time.sleep(0.1)
            state = self._send("?")
            print('[INFO] Sta: ', state)
            
            if(len(state)>1):
               if state[1] == 'I':
                    self.msg.insert('[INFO] State: '+state)
                    break
               elif state[1] == 'A':
                   print("[INFO] Alarm")
                   self.msg.insert("Maquina bloqueada!")
                   self.alarm = True
                   break
            else: break

    def _send(self,code):
        str_send = (code +"\n").encode()
        self.conection.write(str_send)
        #time.sleep(0.001)
        data = self.conection.readline().decode('ascii')
        self.conection.reset_input_buffer()
        return data