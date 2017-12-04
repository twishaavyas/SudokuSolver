"""
Created on Sat Nov 25 15:34:57 2017

@author: Twisha
"""
import tkinter
from  tkinter import *
from tkinter.filedialog import askopenfilename
import sudokuLines

# filename = tkinter.filedialog.askopenfilename() # show an "Open" dialog box and return the path to the selected file
# print(filename)
root = Tk()
root.filename =  askopenfilename(initialdir = "E:\\Robotics\\Sudoku\\project",title = "choose your file")
sudokuLines.Sudoku.solveSudoku(root.filename)