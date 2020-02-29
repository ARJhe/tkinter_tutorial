from tkinter import *
import tkinter as tk
import time as t
from threading import Timer, Thread, Condition, Event
import math, os

currentTime = 0
loopRound = 0
stopFlag = Event()


class Timer(Thread):    
    def __init__(self, event):
        super(Timer, self).__init__()        
        self.stopped = event
        self.daemon = True  # Allow main to exit even if still running.
        self.paused = True  # Start out paused.
        self.state = Condition()        

    def start(self, act=None):
        self.initTime = t.time()        
        btnStart.config(state=DISABLED)
        if act:            
            return super(Timer, self).start()      

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
        btnResume.config(state=NORMAL)
        currentTime = self.timeElape        
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        self.initTime = t.time() # reset initTime   
        btnResume.config(state=DISABLED)
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    def reset(self):
        global currentTime,loopRound        
        loopRound = 0
        currentTime = 0
        self.resume()

    def timeConversion(self,sec):
        _hour = math.floor(sec/3600)
        _min = math.floor(sec/60)
        _sec = math.floor(sec - (_min*60) - (_hour*3600))
        return '%02d : %02d : %02d ' % (_hour,_min,_sec)


root = tk.Tk()
root.geometry('400x300')
root.resizable(0, 0)
root.config(bg='black')
labelText = tk.StringVar()
labelText ='press start'
labScreen = tk.Label(root, text=labelText, fg="white", bg="black",height=5)
labScreen.config(font=("Courier 19 bold"))

iconPATH = os.getcwd() + "\\timer\icons"
print("\33[42m \33[0m Load icons from your directory: \33[35m" + iconPATH)

iconPlay = PhotoImage(file = iconPATH + r"\play.png")
iconPause = PhotoImage(file = iconPATH + r"\pause.png")
iconResume = PhotoImage(file = iconPATH + r"\resume.png")
iconReset = PhotoImage(file = iconPATH + r"\reset.png")
iconExit = PhotoImage(file = iconPATH + r"\exit.png")
iconPy = PhotoImage(file = iconPATH + r"\python-logo.png")
timer = Timer(stopFlag) # Create an instance
btnStart = tk.Button(root ,text='start',command= lambda : timer.start(True), image = iconPlay)
btnStop = tk.Button(root, text='stop', command= timer.pause, image = iconPause)
btnResume = tk.Button(root, text='resume', command= timer.resume, state=DISABLED, image = iconResume)
btnReset = tk.Button(root, text='reset', command= timer.reset, image = iconReset)
btnExit = tk.Button(root, text='Exit',command=root.destroy)
logo = tk.Label(root, image = iconPy)

labScreen.pack(fill='x')
btnStart.place(relx=0.3,rely=0.4)
btnStop.place(relx=0.395,rely=0.4)
btnResume.place(relx=0.5,rely=0.4)
btnReset.place(relx=0.6,rely=0.4)

btnExit.place(relx=0.43,rely=0.7)
btnExit.pack(ipadx=50, pady=50)

logo.place(relx=0.85,rely=0.8)

if __name__ == "__main__":
    root.mainloop()