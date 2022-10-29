import tkinter as tk
from gui.componentframe import ComponentFrame

class SpeedFrame(ComponentFrame):
    def __init__(self,parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.feedrate = tk.IntVar()

        lbl_feedrate = tk.Label(self,text='Feed Rate',font=("Verdana", 12,'bold'),bg='gray90')
        slr_feedrate = tk.Scale(self,from_=250,to=0,orient='vertical',variable=self.feedrate,digits=1,length=150,bg='gray90')

        lbl_feedrate.grid(row=0,column=0,padx=1)
        slr_feedrate.grid(row=1,column=0,rowspan=2)

        self.grid_propagate(0)
        self.config(width=100,height=180,bg='gray90')