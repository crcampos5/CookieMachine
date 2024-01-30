import tkinter as tk
from core.core import Core
from gui.componentframe import ComponentFrame

class RunStopFrame(ComponentFrame):
    def __init__(self,parent) -> None:
        super().__init__(parent)
        self.parent = parent
        #self.config(width=30)

        btn_run = tk.Button(self,text='RUN',font=("Verdana", 18,'bold'),width=6,bg='SeaGreen1', command=self.run)
        btn_pause = tk.Button(self,text='PAUSE',font=("Verdana", 18,'bold'),width=6,bg='gold2', command=self.pause)
        btn_stop = tk.Button(self,text='STOP',font=("Verdana", 18,'bold'),width=6,bg='firebrick1', command=self.stop)



        btn_run.grid(row=0,column=0,padx=22,pady=5)
        btn_pause.grid(row=1,column=0,padx=5)
        btn_stop.grid(row=2,column=0,padx=5,pady=5)

        self.grid_propagate(0)
        self.config(width=160,height=180,bg='gray90')

    def set_core(self,core : Core):
        self.core = core

    def run(self):
        self.core.run()

    def pause(self):
        self.core.pause()

    def stop(self):
        self.core.stop()
    