

import math


class LineGcode:

    def __init__(self,line) -> None:
        self.set_string(line)

    def set_string(self,line):
        letters = ["G","X","Y","Z","F"]
        self.segmentos = {}
        for i in letters:
            print(line)
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

        print(self.segmentos)

    #El angulo tiene que estar convertido a radianes
    def move(self,position,angle):
        x,y = self.segmentos["X"],self.segmentos["Y"]
        x1 = x * math.cos(angle) - y * math.sin(angle)
        y1 = x * math.sin(angle) + y * math.cos(angle) 
        self.segmentos["X"] = x1 + position[0]
        self.segmentos["Y"] = y1 + position[1]

    def get_string(self):
        return "G" + self.segmentos["G"] + " X" + self.segmentos["X"] + " Y" + self.segmentos["Y"] + " Z" + self.segmentos["Z"]

                


                          
                
                