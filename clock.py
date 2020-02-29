from tkinter import *
import tkinter as tk
import time as t
from threading import Timer, Thread, Condition, Event
import math

currentTime = 0
loopRound = 0
stopFlag = Event()

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()    

    def exit(self):
        return super(Interface, self).destroy()

    def hide_me(self, event):
        print('hide me')
        event.widget.place_forget()

class Clock(Thread):    
    def __init__(self, event):
        super(Clock, self).__init__()        
        self.stopped = event
        self.daemon = True  # Allow main to exit even if still running.
        self.paused = True  # Start out paused.
        self.state = Condition()        

    def start(self, act=None):
        self.initTime = t.time()
        if act:            
            return super(Clock, self).start()      

    def run(self):    
        global loopRound    
        self.resume()        
        while not self.stopped.wait(1): # Every 1 second 
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            # Do stuff.
            loopRound += 1
            print("\33[43m \33[0m" " Loop Round:"+ str(loopRound))
            self.timeElape = currentTime + t.time() - self.initTime            
            labScreen['text'] = self.timeConversion(self.timeElape)                

    def pause(self):
        global currentTime
        currentTime = self.timeElape        
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        self.initTime = t.time() # reset initTime   
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    def reset(self):
        global currentTime,loopRound
        self.pause()
        loopRound = 0
        currentTime = 0
        self.resume()

    def timeConversion(self,sec):
        _hour = math.floor(sec/3600)
        _min = math.floor(sec/60)
        _sec = math.floor(sec - (_min*60) - (_hour*3600))
        return '%02d : %02d : %02d ' % (_hour,_min,_sec)


root = Interface()
root.geometry('400x300')
root.resizable(0, 0)
root.config(bg='black')
labelText = tk.StringVar()
labelText ='press start'
labScreen = tk.Label(root, text=labelText, fg="white", bg="black",height=5)
labScreen.config(font=("Courier 19 bold"))

timer = Clock(stopFlag) # Create an instance
btnStart = tk.Button(root ,text='start',command= lambda : timer.start(True))
btnStop = tk.Button(root, text='stop', command= timer.pause)
btnResume = tk.Button(root, text='resume', command= timer.resume)
btnReset = tk.Button(root, text='reset', command= timer.reset)
btnExit = tk.Button(root, text='Quit',command=root.exit, bg='white')

labScreen.pack(fill='x')
btnStart.place(relx=0.25,rely=0.4)
btnStop.place(relx=0.35,rely=0.4)
btnResume.place(relx=0.45,rely=0.4)
btnReset.place(relx=0.6,rely=0.4)
btnExit.place(relx=0.43,rely=0.7)


if __name__ == "__main__":
    root.mainloop()