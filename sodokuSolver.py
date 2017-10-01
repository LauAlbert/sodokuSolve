# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import math

original = np.array([[7, 0, 6, 0, 0, 0, 0, 0, 2], 
                      [0, 3, 0, 9, 0, 0, 0, 0, 0],
                      [0, 0, 4, 1, 0, 0, 6, 0, 0],
                      [0, 7, 5, 2, 0, 0, 0, 0, 0],
                      [0, 0, 0, 4, 0, 7, 0, 0, 0],
                      [0, 0, 0, 0, 0, 8, 2, 9, 0],
                      [0, 0, 8, 0, 0, 5, 7, 0, 0],
                      [0, 0, 0, 0, 0, 6, 0, 5, 0],
                      [5, 0, 0, 0, 0, 0, 1, 0, 6]])

original2 = np.array([[0, 0, 0, 7, 0, 0, 0, 0, 6], 
                      [0, 0, 0, 0, 5, 0, 2, 7, 0],
                      [0, 0, 0, 2, 9, 0, 8, 5, 4],
                      [0, 0, 4, 0, 6, 0, 9, 0, 0],
                      [9, 0, 0, 0, 2, 0, 0, 0, 5],
                      [0, 0, 2, 0, 1, 0, 6, 0, 0],
                      [7, 9, 1, 0, 4, 6, 0, 0, 0],
                      [0, 4, 8, 0, 7, 0, 0, 0, 0],
                      [6, 0, 0, 0, 0, 9, 0, 0, 0]])

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
    
solvePuzzle = solve(0, 0, original)
solvePuzzle2 = solve(0, 0, original2)
