#icons from https://github.com/HaikuArchives/Minesweeper
'''
Beginner level has 5 mines
Intermediate level has 10 mines
Expert level has 40 mines
'''

from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
import random
from tkinter import messagebox
import time
import sys
import platform

sys.setrecursionlimit(10**6)
RIGHT_CLICK = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

class Minesweeper:
    def __init__(self, tk):
        self.tk = tk
        self.images = {
            "cover": ImageTk.PhotoImage(file="image/cover.png"),
            "flag": ImageTk.PhotoImage(file="image/flag.png"),
            "bomb": ImageTk.PhotoImage(file="image/bomb.png"),
            "mine_nums": []
        }
        for i in range(9):
            self.images["mine_nums"].append(ImageTk.PhotoImage(file="image/" + str(i) + ".png"))
        
        self.tiles = {}
        self.mines = []
        self.backup_mine = ""
        self.explore = []
        self.remain_tiles = -1
        self.flag_num = -1
        
        self.frame_level = Frame(self.tk)
        self.frame_level.pack()
        self.frame_grid = Frame(self.tk)
        self.frame_grid.pack()
        self.level()

    # Level selection navbar. Overwrites current game when an option is clicked    
    def level(self):
        ttk.Style().configure('BG.TButton', padding = 6, foreground='black')
        level_1 = ttk.Button(self.frame_level, text="Beginner", style='BG.TButton', command=lambda: self.grid(4,5))
        level_1.pack(side=LEFT)
        level_2 = ttk.Button(self.frame_level, text="Intermediate", style='BG.TButton', command=lambda: self.grid(8,10))
        level_2.pack(side=LEFT)
        level_3 = ttk.Button(self.frame_level, text="Expert", style='BG.TButton', command=lambda: self.grid(16,40))
        level_3.pack(side=LEFT)
    
    # Create a new grid
    def grid(self, gridSize, minesNum):
        for widget in self.frame_grid.winfo_children():
            widget.destroy()
        self.tiles = {}
        self.mines = []
        self.remain_tiles = gridSize*gridSize
        self.flag_num = minesNum
        #set the position of mines
        tiles = []
        for x in range(gridSize):
            for y in range(gridSize):
                tiles.append(str(x)+" "+str(y))
        for i in range(minesNum):
            mine = random.choice(tiles)
            tiles.remove(mine)
            self.mines.append(mine)
        self.backup_mine = random.choice(tiles)
        #set grid
        for x in range(gridSize):
            for y in range(gridSize):
                cover_button = Button(self.frame_grid, image=self.images["cover"])
                cover_button.bind("<Button-1>", self.onClick_helper(x,y,gridSize))
                cover_button.bind(RIGHT_CLICK, self.onRightClick_helper(x,y,gridSize))
                cover_button.grid(row=x+1, column=y)
                pos = str(x)+" "+str(y)
                if pos in self.mines:
                    status = "mine"
                else:
                    status = "clue"
                tile = {
                    "button": cover_button,
                    "status": status,
                    "isFlag": False,
                    "isRevealed": False,
                    "mines_num": 0,
                    "x": x,
                    "y": y
                }
                self.tiles[pos] = tile
        
        #calculate the num of mines nearby
        for x in range(gridSize):
            for y in range(gridSize):
                pos = str(x)+" "+str(y)
                if self.tiles[pos]["status"] == "clue":
                    mines_num = 0
                    nbrs = self.nbrs(x,y,gridSize)
                    for i in nbrs:
                        if self.tiles[i]["status"] == "mine":
                            mines_num += 1
                    self.tiles[pos]["mines_num"] = mines_num
    
    def onClick_helper(self, x, y, gridSize):
        return lambda ev: self.onClick(x,y, gridSize)
    
    #(left)click on tile
    def onClick(self, x, y, gridSize):
        pos = str(x)+" "+str(y)
        #click on the mine on the first hit
        if self.tiles[pos]["status"] == "mine" and self.remain_tiles == gridSize*gridSize:
            self.tiles[pos]["status"] = "clue"
            self.tiles[pos]["isRevealed"] = True
            nbrs = self.nbrs(self.tiles[pos]["x"], self.tiles[pos]["y"], gridSize)
            nbrs_mine = 0
            for i in nbrs:
                if self.tiles[i]["status"] == "mine":
                    nbrs_mine += 1
                self.tiles[i]["mines_num"] = self.tiles[i]["mines_num"] - 1
            self.tiles[pos]["mines_num"] = nbrs_mine
            self.tiles[pos]["button"].configure(image=self.images["mine_nums"][nbrs_mine])
            self.tiles[pos]["button"].unbind(RIGHT_CLICK)
            self.remain_tiles -= 1
            if self.tiles[pos]["isFlag"] == True:
                self.flag_num += 1
            
            self.mines.remove(pos)
            self.mines.append(self.backup_mine)
            self.tiles[self.backup_mine]["status"] = "mine"
            self.tiles[self.backup_mine]["mines_num"] = 0
            backup_nbrs = self.nbrs(self.tiles[self.backup_mine]["x"], self.tiles[self.backup_mine]["y"], gridSize)
            for i in backup_nbrs:
                self.tiles[i]["mines_num"] = self.tiles[i]["mines_num"] + 1
            
            if nbrs_mine == 0:
                self.explore = []
                self.reveal_nbrs(x,y,gridSize)
            
        #click on the mine, game over
        elif self.tiles[pos]["status"] == "mine":
            #show all mines
            for i in range(len(self.mines)):
                pos = self.mines[i]
                self.tiles[pos]["button"].configure(image=self.images["bomb"])
            #quit or restart
            MsgBox = messagebox.askquestion("Game Over", "You Lose :(\nDo you want to play again?")
            if MsgBox == 'yes':
                for widget in self.frame_grid.winfo_children():
                    widget.destroy()
            else:
                self.tk.quit()
        #click on the clue
        else:
            #if the tile is empty, open all non-mine nbrs
            if self.tiles[pos]["mines_num"] == 0 and self.tiles[pos]["isRevealed"] == False:
                self.tiles[pos]["button"].configure(image=self.images["mine_nums"][0])
                self.tiles[pos]["button"].unbind(RIGHT_CLICK)
                self.remain_tiles -= 1
                self.win()
                if self.tiles[pos]["isFlag"] == True:
                    self.flag_num += 1
                self.tiles[pos]["isRevealed"] = True
                self.explore = []
                self.reveal_nbrs(x,y,gridSize)
            else:
                mines_num = self.tiles[pos]["mines_num"]
                self.tiles[pos]["button"].configure(image=self.images["mine_nums"][mines_num])
                self.tiles[pos]["button"].unbind(RIGHT_CLICK)
                self.remain_tiles -= 1
                self.win()
                if self.tiles[pos]["isFlag"] == True:
                    self.flag_num += 1
                self.tiles[pos]["isRevealed"] = True

    def onRightClick_helper(self, x, y, gridSize):
        return lambda ev: self.onRightClick(x,y, gridSize)
    
    # Right click to place a flag. The number of flags cannot exceed the number of mines.
    def onRightClick(self, x, y, gridSize):
        pos = str(x)+" "+str(y)
        if self.flag_num != 0 and self.tiles[pos]["isFlag"] == False:
            self.tiles[pos]["button"].configure(image=self.images["flag"])
            self.flag_num -= 1
            self.tiles[pos]["isFlag"] = True
        elif self.flag_num == 0 and self.tiles[pos]["isFlag"] == False:
            messagebox.showwarning("Warning", "Too many flags!")
        elif self.tiles[pos]["isFlag"] == True:
            self.tiles[pos]["button"].configure(image=self.images["cover"])
            self.flag_num += 1
            self.tiles[pos]["isFlag"] = False
            self.tiles[pos]["button"].bind("<Button-1>", self.onClick_helper(x,y,gridSize))
                
    # Returns a list of x y coordinates, used by reveal_nbrs to show revealed tiles.
    def nbrs(self, x, y, gridSize):
        nbrs = []
        if x-1>=0 and y-1>=0:
            nbrs.append(str(x-1)+" "+str(y-1))
        if x-1>=0:
            nbrs.append(str(x-1)+" "+str(y))
        if x-1>=0 and y+1<gridSize:
            nbrs.append(str(x-1)+" "+str(y+1))
        if y-1>=0:
            nbrs.append(str(x)+" "+str(y-1))
        if y+1<gridSize:
            nbrs.append(str(x)+" "+str(y+1))
        if x+1<gridSize and y-1>=0:
            nbrs.append(str(x+1)+" "+str(y-1))
        if x+1<gridSize:
            nbrs.append(str(x+1)+" "+str(y))
        if x+1<gridSize and y+1<gridSize:
            nbrs.append(str(x+1)+" "+str(y+1))
        return nbrs
    
    # Display number tiles, recursively explore to reveal.
    def reveal_nbrs(self, x, y, gridSize):
        nbrs = self.nbrs(x,y,gridSize)
        # print(nbrs)
        for i in nbrs:
            if self.tiles[i]["status"] == "clue" and self.tiles[i]["isRevealed"] == False and i not in self.explore:
                mines_num = self.tiles[i]["mines_num"]
                self.tiles[i]["button"].configure(image=self.images["mine_nums"][mines_num])
                self.tiles[i]["button"].unbind(RIGHT_CLICK)
                self.tiles[i]["isRevealed"] = True
                self.remain_tiles -= 1
                self.win()
                if self.tiles[i]["isFlag"] == True:
                    self.flag_num += 1
                self.explore.append(i)
                if mines_num == 0:
                    self.reveal_nbrs(self.tiles[i]["x"], self.tiles[i]["y"], gridSize)
    
    # Display message box if won
    def win(self):
        if self.remain_tiles == len(self.mines):
            MsgBox = messagebox.askquestion("Game Over", "You Win :)\nDo you want to play again?")
            if MsgBox == 'yes':
                for widget in self.frame_grid.winfo_children():
                    widget.destroy()
            else:
                self.tk.quit()
            
def main():
    root = Tk()
    root.title("Minesweeper")
    minesweeper = Minesweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main()
