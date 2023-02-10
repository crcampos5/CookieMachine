

class LineGcode:

    def __init__(self) -> None:
        self.g = ""
        self.x = 0
        self.y = 0
        self.z = 0
        self.f = 0
        self.s = ""
        self.m = ""

    def set_string(self,line):
        g = line.find('G')
        x = line.find('X')
        y = line.find('Y')
        z = line.find('Z')
        f = line.find('F')

        if g :
            if x and y and z and f:
                self.x = line[x+1:y]
                self.y = line[y+1:z]
                self.z = line[z+1:f]
                self.f = line[f+1:len(line)]
            if x and y and z:
                self.x = line[x+1:y]
                self.y = line[y+1:z]
                self.z = line[z+1:len(line)]
            if x and y:
                self.x = line[x+1:y]
                self.y = line[y+1:len(line)]
                


                          
                
                