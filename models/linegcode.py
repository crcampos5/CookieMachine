

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
                


                          
                
                