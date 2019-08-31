import tkinter as tk
import time as t
from threading import Timer
import math

root = tk.Tk()
root.geometry('500x300')

conti = True
class Clock():
    global btn_text, conti
    def __init__(self):
        self.init_time = t.time()
        self.timer()


    def timer(self):
        recall = Timer(1.0, self.timer)
        if conti:
            start['text'] = 'stop'
            time_elape = t.time() - self.init_time
            label['text']= self.formater(time_elape)
            recall.start()
        elif not conti:
            recall.cancel()
        
    def formater(self,sec):
        _hour = math.floor(sec/3600)
        _min = math.floor(sec/60)
        _sec = math.floor(sec - (_min*60) - (_hour*3600))
        return '%02d hour %02d min %02d sec' % (_hour,_min,_sec)

def stop1():
    global conti
    conti = False

def exit():
    root.destroy()

var = tk.StringVar()
var ='press start'
btn_text = tk.StringVar()
# lambda create instance of Clock()
# automatic initalize init time
start = tk.Button(root ,text='start',
                    command= lambda : Clock())
start.pack()
stop_btn = tk.Button(root, text='stop!', command= stop1)
stop_btn.pack()
label = tk.Label(root, text=var)
label.pack()
quit = tk.Button(root, text='Quit',command=exit)
quit.pack()
root.mainloop()