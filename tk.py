import tkinter as tk
import time as t
from threading import Timer
import math

root = tk.Tk()
root.geometry('500x300')

var = tk.StringVar()
var ='press start'
# lambda create instance of Clock()
# automatic initalize init time
start = tk.Button(root ,text='start',
                    command= lambda : Clock())
label = tk.Label(root, text=var)

# overwrite run method
class ReapeatTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)

class Clock():
    def __init__(self):
        self.init_time = t.time()
        self.timer()

    def timer(self):
        recall = ReapeatTimer(1.0,self.timer)
        time_elape = t.time() - self.init_time
        label['text']= self.formater(time_elape)
        recall.start()

    def formater(self,sec):
        _hour = math.floor(sec/3600)
        _min = math.floor(sec/60)
        _sec = math.floor(sec - (_min*60) - (_hour*3600))
        return '%02d hour %02d min %02d sec' % (_hour,_min,_sec)

start.pack()
label.pack()
quit = tk.Button(root, text='Quit',
                    command=root.destroy)
quit.pack()


root.mainloop()