#-*- coding: utf-8 -*-
# Author: ArJhe
from tkinter import *
from time import time as t
import sys

root = Tk()
root.geometry("700x470")
root.config(bg='#ffac3c')
black = True
tracks = 15

class boardFrame(Canvas):
    def __init__(self, master= None, height=0, width=0):
        # 1. drew a line in root
        global tracks
        super(boardFrame, self).__init__(master, height=height, width=height)
        self.initBoardFrame(tracks)         
        self.config(bg='#ffac3c')  
        self.bind("<Key>", self.key)
        self.bind("<Button-1>", self.callback)
        self.boardAssitant = boardInfo()                
        self.pack()
        self.text = StringVar()
        self.text = 'game start!!'        
        self.widget = Label(self, text=self.text, fg='black', bg='#ffac3c', font=("Courier", 20))
        self.clacu =  Label(self, text='', fg='white', bg='black')
        self.widget.pack()
        self.clacu.pack()
        self.create_window(580, 150, window=self.widget) 
        self.create_window(530, 430, window=self.clacu)
        self.resetGame = Button(self, text = "重新開始", command = self.reset, anchor = W)
        self.resetGame.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        self.create_window(610, 420, anchor=NW, window=self.resetGame)
        
    def reset(self):
        global black
        self.delete("stone")
        self.boardAssitant.clear()
        black = True
        self.widget['text'] ="black's turn"
        self.bind("<Button-1>", self.callback)
        self.clacu['text'] = ''
    def initBoardFrame(self, tracks): # Default tracks: 15
        for dir in ['v', 'h']:# If direction equals to 'v', draw vertical lines else horizon lines.                        
            for i in range(tracks):# ixp: initial x-axis point; iyp: initial y-axis point; 
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
        self.create_oval(ixp, iyp, exp, eyp, fill= 'black')

    def placeStone(self, col, row, color='black'):  # placing stone
        r = 12.5  # radius
        row , col = (row)*30, (col)*30
        circle = tuple([col-r,row-r,col+r, row+r])
        self.create_oval(circle, fill= color, tag='stone')        

    def key(self, event):
        print("pressed", repr(event.char))
        if repr(event.char) == "'\\x1b'": # Press Esc to exit
            self.master.destroy()

    def callback(self, event):
        global black
        self.focus_set()
        print("clicked at", event.x, event.y)
        if event.x < 16 or event.x > 464 or event.y < 16 or event.y > 464:
            return
        x, y = self.boardAssitant.findPosition(event.x, event.y)  # return column, row 31,63 [c0,r1]
        r,c = y-1, x-1  # fetch position info, matrix initialize from 0,0
        placed = self.boardAssitant.check(r, c)
        # 30/30, 450/30, 450/450, 30/450        
        if not placed:
            if black:
                stoneColor = 'black'
                self.placeStone(x, y, stoneColor)            
                black = False
                self.boardAssitant.boardInfo[r][c]= 1
                self.widget['text'] ="white's turn"                
            else:
                stoneColor = 'white'
                self.placeStone(x, y, stoneColor)
                black = True
                self.boardAssitant.boardInfo[r][c]= -1
                self.widget['text'] ="black's turn"            
            print('row: {}, column: {} has been placed {} stone'.format(r, c, stoneColor))
            # print(self.boardAssitant.boardInfo)
            _color = 1 if stoneColor == 'black' else -1
            self.ajacency(r,c, _color)
            
    def ajacency(self, row, col, color):
        '''
            After placing stone, check near stones one by one if is same color.
            If so, +1 point and move to next alone that direction, 
            sumup with 4 direction total point.
        '''        
        global black
        init = t ()        
        directions = self.boardAssitant.directions                
        for direction in directions.keys():
            win = self.boardAssitant.sums(row, col, direction, color)            
            if win:
                _color = 'black' if color == 1 else 'white'
                self.widget['text'] = ' {} win,\nGame over'.format(_color)              
                self.unbind("<Button-1>")
        deltaTime = round(t()- init, 4)
        print('time elapes: {}'.format(deltaTime))
        self.clacu['text'] = '檢查所費時間: {} 秒'.format(deltaTime)       

class boardInfo():
    def __init__(self):
        global tracks
        self.boardInfo = []
        self.directions = {'vertical' : [1,0], 'horizen': [0,1] , 'oblique': [-1,1], 'backslash': [-1,-1]}
        for _r in range(tracks):  # create a matrix record board info
            self.boardInfo.append([None for _c in range(tracks)])
        self.restartBox = self.boardInfo

    def check(self, row, column):
        '''
        check board specific postion's info: black, white or None
        return: 1, -1, None
        '''
        global tracks
        if row>=0 and row<=tracks-1 and column>=0 and column<= tracks-1:
            return self.boardInfo[row][column]
    
    def sums(self, r, c, direction,color):
        '''
        sumup points and check if win
        '''
        points = 0
        startPosition = [r, c]
        _next = self.directions[direction]
        _revers = list((_next[0]*-1, _next[1]*-1))
        reverseR, reverseC = startPosition[0]+_revers[0], startPosition[1]+ _revers[1]
        while True:
            if self.check(r,c) == color:
                points += 1
                r+= _next[0]
                c+= _next[1]
            elif self.check(reverseR, reverseC) == color:
                points += 1
                reverseR += _revers[0]
                reverseC += _revers[1]
            else:                
                print('{} {} totla points :{}'.format(color,direction, points))
                if points>=5:
                    return True                
                break

    def findPosition(self, x, y): 
        column = int(round(x/30,0))
        row = int(round(y/30,0))
        return column, row

    def clear(self):
        global tracks
        restart = [[None for _ in range(tracks)] for __ in range(tracks)]
        self.boardInfo = restart


game = boardFrame(root, height=800, width=600)




if __name__ == "__main__":
    root.mainloop()