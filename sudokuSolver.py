# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 22:30:16 2017

@author: Albert-Desktop
"""

import cv2
import math
import numpy as np
from keras.models import load_model

# load trained CNN model (created from cnn.py)
model = load_model('my_model.h5')

# read in a picture of a sudoku puzzle
sudokuPuzzle = cv2.imread("sudoku.png")
h, w, c = sudokuPuzzle.shape

sudoku = []

for row in range(9):
    sudokuRow = []
    for col in range(9):
        x = int(w/9) * col
        y = int(h/9) * row
        crop_img = sudokuPuzzle[y:y+int(h/9), x:x+int(w/9)] # Crop from x, y, w, h -> 100, 200, 300, 400
        # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
        gray_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(gray_img, (28,28))
        img = 255-img
        img = img.reshape(1, 28, 28, 1)
        sudokuRow.append(np.argmax(model.predict(img)))

    sudoku.append(sudokuRow)
    



# Algorithm to solve the Sodoku Puzzle
sudoku = np.array(sudoku)
possibleValues = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]



def getNext(row, col):
    if (col == 8):
        return [row+1, 0]
    else:
        return [row, col+1]

def solve(row, col, puzzle):
    puzzleCopy = np.copy(puzzle)
    nextitem = getNext(row, col)
    # 0 mean empty
    # try to find value for the cell
    if (puzzle[row, col] == 0):
        sectionRow = math.floor(row/3)*3
        sectionCol = math.floor(col/3)*3
        usedValues = set([*list(puzzle[:, col]), *list(puzzle[row,:]), *list(puzzle[sectionRow: sectionRow+3, sectionCol: sectionCol+3].flatten())])
        availableValues = list(usedValues^set(possibleValues))
        if (row == 8 and col == 8):
            puzzleCopy[row, col] = availableValues[0]
            return puzzleCopy
        else:
            for availableValue in availableValues:
                puzzleCopy[row, col] = availableValue
                found = solve(nextitem[0], nextitem[1], puzzleCopy)
                if (found is not None):
                    return found
            return None;
    else:
        if (row == 8 and col == 8):
            return puzzleCopy
        found = solve(nextitem[0], nextitem[1], puzzleCopy)
        if (found is not None):
            return found
        return None
    
solvePuzzle = solve(0, 0, sudoku)

print(solvePuzzle)        