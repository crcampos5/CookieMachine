import serial.tools.list_ports
import time

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
            print("Port Product", i.product)
            self.port = i.device
        return [self.port]

    def connect_serial(self):
        self.conection = serial.Serial(self.port, baudrate = 115200, timeout = 2)
        self.msg.insert("Conectado a la maquina")
        #time.sleep(0.1)

    def move(self,axis,value):
        print("mover")
        code = 'G1 '+ axis + str(value)
        data = self._send(code)
        print(data)
        self.wait_idle()

    def disable_alarm(self):
        self.msg.insert("Desbloqueando...")
        self._send("$X")
        #self.wait_idle()
        self.msg.insert("Maquina desbloqueada")

    def wait_idle(self):
        while True:
            state = self._send("?")
            print('[INFO] State: ', state)
            if(len(state)>1):
               if state[1] == 'I':
                   break
               elif state[1] == 'A':
                   print("[INFO] Alarm")
                   self.alarm = True
                   break
            else: break

    def _send(self,code):
        str_send = (code +"\r\n").encode()
        self.conection.write(str_send)
        #time.sleep(0.001)
        data = self.conection.readline().decode('ascii')
        self.conection.reset_input_buffer()
        return data