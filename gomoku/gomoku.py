#-*- coding: utf-8 -*-
from tkinter import *

root = Tk()
root.geometry("700x470")
root.config(bg='#ffac3c')

class boardFrame(Canvas):
    def __init__(self, tkr= None, height=0, width=0):
        # 1. drew a line in root
        super(boardFrame, self).__init__(tkr, height=height, width=height)
        self.initBoardFrame()
        self.config(bg='#ffac3c')
        self.pack()

    def initBoardFrame(self, tracks=15): # Default tracks: 15
        for dir in ['v', 'h']: # If direction equals to 'v', draw vertical lines else herizen lines.                        
            for i in range(tracks):
                # ixp: initial x-axis point; iyp: initial y-axis point
                # exp: end x-axis point; eyp: end y-axis point
                ixp = 30*i + 30 if dir=='v' else 30
                iyp = 30 if dir=='v' else 30*i + 30
                exp = 30*i + 30 if dir=='v' else tracks*30
                eyp = tracks*30 if dir=='v' else 30*i + 30
                self.create_line(ixp, iyp, exp, eyp)

        mid = int(tracks/2)
        ini = int(mid/2)
        quo = int(mid/2+tracks/2)    
        starPosition = [(ini,ini),(quo,ini),(mid,mid),(ini,quo),(quo,quo)]        
        for pos in starPosition:
            self.pinStar(pos[0], pos[1])

    def pinStar(self, row, col):
        ixp = 30*row + 28
        iyp = 30*col + 28
        exp = 30*row + 32
        eyp = 30*col + 32
        self.create_oval(ixp, iyp, exp, eyp, fill = 'black')



        
game = boardFrame(root, height=800, width=600)



if __name__ == "__main__":
    root.mainloop()