#-*- coding: utf-8 -*-
from tkinter import *
import time as t
from threading import Timer, Thread, Condition, Event
import math, os

""" Can execute by zipping lib and py file by cmd: 
pyinstaller -F --noconsole --onefile .\Timer.py
"""

currentTime = 0 # Catch value of current t.time() while paused
loopRound = 0
stopFlag = Event() # Role of passing signal to pause thread
isReset = False
class myTimer(Thread): # Like a Rockman inherited Thread's methods and attributes.
    def __init__(self, event):
        super(myTimer, self).__init__()        
        self.stopped = event
        self.daemon = True  # Allow main to exit even if still running.
        self.paused = True  # Start out paused.
        self.state = Condition()        

    def start(self, act=None): # overwrite
        # Defaultly assign None to parameter "act" to avid activating "initTime" 
        # while class "myTimer" was called.
        global currentTime, isReset, loopRound
        self.initTime = t.time()        
        btnStart.config(state=DISABLED)        
        labScreen['text'] = self.timeConversion(0)
        # Check whether is reset and activate by btnStart or not
        if act and not isReset:
            return super(myTimer, self).start()      
        else:
            # Re-click start resume can avoid 
            # self._started.is_set() check(threading.py Line 847)
            loopRound = 0
            currentTime = 0
            self.resume()

    def run(self): # Overwrite
        global loopRound    
        self.resume()        
        while not self.stopped.wait(1): # Execute only after 1 second 
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
        self.initTime = t.time() # Reset initTime
        btnResume.config(state=DISABLED)
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    def reset(self):
        global isReset                
        isReset = True               
        btnStart.config(state=NORMAL)
        btnResume.config(state=DISABLED)  
        labScreen['text'] = self.timeConversion(0)
        self.pause()
    
    def timeConversion(self,sec):
        _hour = math.floor(sec/3600)
        _min = math.floor(sec/60)
        _sec = math.floor(sec - (_min*60) - (_hour*3600))
        return '%02d : %02d : %02d ' % (_hour,_min,_sec)

root = Tk()
root.geometry('400x300')
root.resizable(0, 0)
root.config(bg='black')
labelText = StringVar()
labelText ='press start'
labScreen = Label(root, text=labelText, fg="white", bg="black",height=5)
labScreen.config(font=("Courier 19 bold"))

iconPATH = os.getcwd() + "\\Timer\icons"
print("\33[42m \33[0m Load icons from your directory: \33[35m" + iconPATH)

iconPlay = PhotoImage(file = iconPATH + r"\play.png")
iconPause = PhotoImage(file = iconPATH + r"\pause.png")
iconResume = PhotoImage(file = iconPATH + r"\resume.png")
iconReset = PhotoImage(file = iconPATH + r"\reset.png")
iconExit = PhotoImage(file = iconPATH + r"\exit.png")
iconPy = PhotoImage(file = iconPATH + r"\python-logo.png")
iTimer = myTimer(stopFlag) # Call myTimer to Create an instance
btnStart = Button(root ,text='start',command= lambda : iTimer.start(True), image = iconPlay, cursor="hand2")
btnStop = Button(root, text='stop', command= iTimer.pause, image = iconPause, cursor="hand2")
btnResume = Button(root, text='resume', command= iTimer.resume, state=DISABLED, image = iconResume, cursor="hand2")
btnReset = Button(root, text='reset', command= iTimer.reset, image = iconReset, cursor="hand2")
btnExit = Button(root, text='Exit', font= ("Courier 14 bold"),command=root.destroy, cursor="hand2")
logo = Label(root, image = iconPy)

labScreen.pack(fill='x') # Fill up x-axis.
btnStart.place(relx=0.3,rely=0.4) # .palce(positioning)
btnStop.place(relx=0.395,rely=0.4)
btnResume.place(relx=0.5,rely=0.4)
btnReset.place(relx=0.6,rely=0.4)

btnExit.place(relx=0.43,rely=0.7)
btnExit.pack(ipadx=50, pady=50)

logo.place(relx=0.85,rely=0.8)

if __name__ == "__main__":
    root.mainloop()