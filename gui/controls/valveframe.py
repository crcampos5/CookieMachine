import tkinter as tk
from gui.componentframe import ComponentFrame

class ValveFrame(ComponentFrame):
    def __init__(self,parent) -> None:
        super().__init__(parent)
        self.parent = parent

        btn_home = tk.Button(self,text='HOME',font=("Verdana", 14,'bold'),width=6)
        btn_valve = tk.Button(self,text='VALVE',font=("Verdana", 14,'bold'),width=6)


        btn_home.grid(row=0,column=0,padx=5,pady=10)
        btn_valve.grid(row=1,column=0,padx=5)

       

        self.grid_propagate(0)
        self.config(width=100,height=180,bg='gray90')