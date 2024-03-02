import threading
import serial.tools.list_ports
import time
from core.observer import Observer
from core.parametros import Parametros
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
        self.lista_puertos = []
        self.alarm = False
        self.ishome = False
        self.isconect = False
        self.stop_ban = False
        self.laser_on = False
        self.is_run = True
        self.conection = None

        self.parameters = Parametros()

        self.find_port()
        self.modes = self.parameters.get_parametro("modes")
        self.feed_scan = 400
        self.selected_mode = self.modes["Boquilla"]
        self.laser_intensity = self.parameters.get_parametro("laser_intensity")
        

        

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
            self.lista_puertos.append(i.device)
            self.port = i.device
            
    def set_parameters(self,parameters):
        self.parameters = parameters
        
    #establece la conexión serial con la máquina CNC
    def connect_serial(self, port, is_open):
        self.port = port
        self.isconect = is_open
        if self.isconect == True :
            self.conection = serial.Serial(self.port, baudrate = 115200, timeout = 2)
            self.msg.insert("Conectado a la maquina")
            self._send("G10 P1 L20 X0 Y0 Z0")
            self.wait_idle()
        else :
            self.conection.close()
            self.msg.insert("Cerrando conexion con la maquina")
            self.isconect = False
        #time.sleep(0.1)
            
    def closecnc(self):
        if self.conection != None :
            self.laser_onoff(False)
            self.conection.close()

    #envía la señal de "home" a la máquina CNC para mover sus ejes a las coordenadas de origen    
    def home(self):
        #estado = self._send("$G")
        code = "$H"
        data = self._send(code)
        print("Home: ", data)
        self.msg.insert("Haciendo Home")
        self.wait_idle()
        self.ishome = True

    def reset(self):
        #estado = self._send("$G")
        code = "^X"
        data = self._send(code)
        print("Reset: ", data)
        self.msg.insert("La maquina ha sido reseteado")
        self.wait_idle()
        self.ishome = True

    #mueve un eje de la máquina CNC a una posición específica    
    def move(self,axis,value):
        if self._check():
            self.wait_idle()
            code = "$J=G21G91"+axis+str(value)+"F"+str(self.pos.F)
            data = self._send(code)
            print("data",data)
            self.wait_idle()
            return "Termino"
        else : "No se pudo ejecutar el comando"

    #mueve la máquina CNC a una posición en el plano X-Y
    def movexy(self,x,y,mode = "Boquilla"):
        if self._check():
            offset_xy = self.modes[mode]
            x = str(x + offset_xy[0])
            y = str(y + offset_xy[1])
            code = "G0G90 X"+ x + " Y" + y
            data = self._send(code)
            self.wait_idle()

    #Esta función se encarga de mover un escáner a una posición específica
    #en el eje X e Y, capturar imágenes con una cámara y devolver una lista de imágenes escaneadas.
    
    def move_scan(self,x,y,cap, d = 100):
        offset_xy = self.modes["Laser"] #Obtiene la compensacion para las coordenadas X e Y del modo de escaneo láser.
        c = x - d + offset_xy[0] + 1 #Calcula la coordenada X inicial para el escaneo
        c_final = c + d  
        print("c inicial: ", c)
        x = str(x + offset_xy[0]) #Ajusta las coordenadas x e y con el offset obtenido anteriormente.
        y = str(y + offset_xy[1])
        self.laser_onoff(True)
        q = 0
        # Se ejecuta el siguiente while para darle tiempo a la camara que ajuste sus parametros 
        while q < 3:
            a_time = time.time()
            ret, imagen = cap.read()
            b_time = time.time()
            print("Video time: ", b_time - a_time)
            q += 1
        
        list_images = []
        code = "G1 X"+ x + " Y" + y + " F" + self.feed_scan
        str_send = (code +"\n").encode()
       
        start_time = time.time()
        self.conection.write(str_send)
        self.conection.reset_input_buffer()       
        #Envía un comando para obtener la posición actual del escaner.
        #Lee la respuesta del escáner.
        #Comprueba si la posición actual coincide con la posición deseada para escanear. 
        #Si coincide, captura una imagen utilizando la cámara y la agrega a list_images.
        while 1 :
            time.sleep(0.03) # este parametro esta relacionado con feed scan            
            str_send = ("?\n").encode()
            self.conection.write(str_send)
            data = self.conection.readline().decode('ascii')
            self.conection.reset_input_buffer()
            if "MPos" in data:
                #a = data.split("|")
                a = data.find("MPos") + 5
                b = data.find("F") - 1
                x,y,z = data[a:b].split(',')
                w = int(float(x))
                #print("c,x: ",c , w)
                if c == w:
                     #a_time = time.time()
                     ret, imagen = cap.read()
                     if ret:
                        list_images.append(imagen)
                     #b_time = time.time()
                     #print("Imagen mm: ", c)
                     c += 1
                if c == c_final: 
                    break
                if c < w : 
                    print("Fallo al escanear")
                    break
                
            
        end_time = time.time()

        print("Time: ", end_time - start_time )
        print("Cantidad de imagenes: ", len(list_images))
        self.laser_onoff(False)
        return list_images


    def move_to_quadrant(self,mode = "Boquilla"):
        quadrant = self.parameters["quadrants"][0]
        self.movexy(quadrant[0],quadrant[1],mode)
        
    #desbloquea la máquina CNC en caso de que esté en estado de alarma
    def disable_alarm(self):
        self.msg.insert("Desbloqueando...")
        self._send("$X")
        self.wait_idle()
        self.alarm = False
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
            if self.stop_ban == False:
                number_line += 1
                code = line.get_string()
                #print(code)
                out = self._send(code)
                if out == "ALARM":
                    self.msg.insert(out)
                    self.notify()
                    break
                if number_line % 10 == 0:
                    state = self._send("?")
                    #print('[INFO] State: ', state)
                    sigo = self.process_out(state)
            else:  break
    #envía una lista de comandos Gcode a la máquina CNC para ser ejecutados es mas rapido
    def ejecutar_gcode2(self,gcode):
        start_time = time.time()
        number_line = 0
        if len(gcode) == 0:
            print("No hay lineas a ejecutar")
        error = False
        for line in gcode:
            if error  == False:
                number_line += 1
                code = line.get_string()
                self.conection.write((code +"\n").encode())
                print(code)
                while(1): # Wait untile the former gcode has been completed.
                    data = self.conection.readline().decode()
                    if data.startswith('ok'):
                        print("ok")
                        break
                    if data.startswith('ALARM') :
                        error = True
                        print (data)
                        break
               
        end_time = time.time()

        print("Time: ", end_time - start_time )
            

    
    def save_gcode(self,gcode):
            #self.status.start()
        number_line = 0
        if len(gcode) == 0:
            print("No hay lineas a guardar")
        f = open ('gcode.txt','w')
        for line in gcode:
            number_line += 1
            code = line.get_string()
            f.write('\n' + code)

        f.close()     
           


    def _send(self,code):
            str_send = (code +"\n").encode()
            self.conection.write(str_send)
            #time.sleep(0.001)
            data = self.conection.readline().decode('ascii')
            self.conection.reset_input_buffer()
            return data

    def process_out(self,data):
        if len(data)>1 : #  and "<" in data:
            #print('[INFO] State: ', data)
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
    def laser_onoff(self, ban: bool):
        if self._check():
            self.laser_on = ban
            if self.laser_on :
                self.msg.insert("Activando laser")
                data = self._send("G1 S" + str(self.laser_intensity) +"F100")
                print(data)
                data = self._send("M3")
            else :
                data = self._send("M5")
                self.msg.insert("Desactivando laser")
                print(data)

            self.notify()
        else : return False
        

    def laserpower(self, p):
        if self._check():    
            self.laser_intensity = p
            code = "G1 S" + str(p) + " F100"
            data = self._send(code)
            return True
        else : return False
            
       

    def pause(self):
        if self._check():
            self.msg.insert("Pausando...")
            self._send("!")
            self.wait_idle()
            self.msg.insert("Maquina pausada")

    def stop(self):
        self.msg.insert("Parando...")
        self.stop_ban = True
        self.msg.insert("Maquina parada")

    def _check(self):
        if self.isconect : return True
        else : 
            self.msg.insert("Maquina esta desconectada")
            return False

        

