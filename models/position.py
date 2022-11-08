

class Position:
    def __init__(self) -> None:
        self.X = 1.0
        self.Y = 0.0
        self.Z = 0.0
        self.F = 100
    
    def set_displays(self,disx,disy,disz):
        self.disx = disx
        self.disy = disy
        self.disz = disz
        self.set_pos(self.X,self.Y,self.Z)

    def set_pos(self,x,y,z):
        self.X = x
        self.Y = y
        self.Z = z
        self.disx.config(text = str(x))
        self.disy.config(text = str(y))
        self.disz.config(text = str(z))
