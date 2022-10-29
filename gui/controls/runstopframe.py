import tkinter as tk
from gui.componentframe import ComponentFrame

class RunStopFrame(ComponentFrame):
    def __init__(self,parent) -> None:
        super().__init__(parent)
        self.parent = parent
        #self.config(width=30)

        btn_run = tk.Button(self,text='RUN',font=("Verdana", 18,'bold'),width=6,bg='SeaGreen1')
        btn_pause = tk.Button(self,text='PAUSE',font=("Verdana", 18,'bold'),width=6,bg='gold2')
        btn_stop = tk.Button(self,text='STOP',font=("Verdana", 18,'bold'),width=6,bg='firebrick1')



        btn_run.grid(row=0,column=0,padx=22,pady=5)
        btn_pause.grid(row=1,column=0,padx=5)
        btn_stop.grid(row=2,column=0,padx=5,pady=5)

        self.grid_propagate(0)
        self.config(width=160,height=180,bg='gray90')