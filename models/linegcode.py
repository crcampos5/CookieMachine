

import math


class LineGcode:

    def __init__(self,line) -> None:
        self.set_string(line)

    def set_string(self,line):
        letters = ["G","X","Y","Z","F"]
        self.segmentos = {}
        for i in letters:
            #print(line)
            l = line.find(i)
            if l >= 0:
                s = line.split(i)[1]
                a = 0
                for j in letters:
                    p = s.find(j)
                    if p >= 0:
                        a += 1
                        self.segmentos[i] =  float(s[0:p])
                        line = s
                        break
                if a == 0 : self.segmentos[i] =  float(s)

        #print(self.segmentos)

    #El angulo tiene que estar convertido a radianes
    def move(self,position,angle):
        if "X" in self.segmentos and "Y" in self.segmentos:
            #print("segmentos: ", self.segmentos)
            x,y = self.segmentos["X"],self.segmentos["Y"]
            x1 = x * math.cos(angle) - y * math.sin(angle)
            y1 = x * math.sin(angle) + y * math.cos(angle) 
            self.segmentos["X"] = y1 + position[0]
            self.segmentos["Y"] = x1 + position[1]

    def get_string(self):
        g = ""
        if self.segmentos:
            if "G" in self.segmentos:
                g  += "G" + str(int(self.segmentos["G"]))
            if "X" in self.segmentos:
                g += " X" + str(round(self.segmentos["X"],3))
            if "Y" in self.segmentos:
                g += " Y" + str(round(self.segmentos["Y"],3))
            if "Z" in self.segmentos:
                g += " Z" + str(round(self.segmentos["Z"],3))
            if "F" in self.segmentos:
                g += " F" + str(self.segmentos["F"])
        
        return g
    
    def contains_z(self):
        if "Z" in self.segmentos: return True | False

    def get_z (self):
        if "Z" in self.segmentos:
            return self.segmentos["Z"]
        else : return None

    def set_z(self,z):
        if "Z" in self.segmentos:
            self.segmentos["Z"] = float(z)
            return True
        else : return False

                
    

                          
                
                