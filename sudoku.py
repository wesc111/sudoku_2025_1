#!/usr/local/bin/python3

""" program to solve SUDOKUs by finding unique candidates
For command description, start $python3 sudoku.py -help
"""

VERSION = "0.1"
VERSION_DATE = "18-Feb-2025"

# file name of input file with SUDOKUs
SU_FILE_NAME = "easy_50.txt"
#SU_FILE_NAME = "sudoku_1.txt"

DEBUG_LEVEL = 1

# select the SUDOKUs to be solved by their number in the file
# for example, to solve SUDOKUs 6,7 and 10, set SU_NUM_LIST = [6,7,10]
SU_NUM_LIST = [1]
# for case that all SUDOKUs in the file should be solved, set SOLVE_ALL = True
# in this case, the list SU_NUM_LIST is ignored
SOLVE_ALL = False

from sudoku_io import sudoku_io
from sudoku_p1 import sudoku

def getBoard(sudokuText):
    """convert a SUDOKU in text form to a 9x9 list"""
    if len(sudokuText) != 81:
        print("Error: SUDOKU text has not the correct length")
        return None
    board = []
    i=0
    for row in range(0,9):
        vector = []
        for col in range(0,9):
            if sudokuText[i] == ".":  # empty element is represented by a dot
                vector.append(0)
            else:
                vector.append(int(sudokuText[i]))
            i += 1
        board.append(vector)
    return board

# ------------------------------------------------------------------------------------------------
# main program
# ------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    suSolvedInfo = {}
    # read the input file into arrays suText, suComment
    myIo = sudoku_io()
    print(f"... reading file name {SU_FILE_NAME}")
    numRead = myIo.readFile(SU_FILE_NAME)
    suTextList, suCommentList = myIo.getSudokuList()   
    fNum=1
    # loop over all SUDOKUs
    for su in suTextList:
        comment = suCommentList[fNum-1]
        if SOLVE_ALL or (fNum in SU_NUM_LIST):
            board =  getBoard(su)
            # create a sudoku object
            if board is None:
                print(f"Error: SUDOKU {fNum} is not valid")
                fNum += 1
                continue
            print(f"\n===== SUDOKU: {fNum} ({comment}) =====")
            s = sudoku(board)
            s.setDebugLevel(DEBUG_LEVEL)
            print(s)   
            # try to solve the SUDOKU
            s.solve()
            print(f"\n===== SUDOKU {fNum} ({comment}) after solving =====")
            print(s)
            s.printStatistics()
            suSolvedInfo[fNum] = {"solved":s.isSolved(), "unique":s.numUniqueCandidatesFound, "hidden":s.numHiddenSinglesFound, "loops":s.loopCount, "comment":s.comment}
        fNum += 1   

    print("\n===== SUMMARY of all SUDOKUs =====")
    for elem in suSolvedInfo:
        print(f"SUDOKU {elem}: {suSolvedInfo[elem]['comment']}")
        print(f"{'   ... SOLVED ' if suSolvedInfo[elem]['solved'] else '   ... NOT SOLVED '}",end="")
        print(f"with {suSolvedInfo[elem]['unique']} unique candidates, ",end="")
        if suSolvedInfo[elem]['hidden']>0:
            print(f"{suSolvedInfo[elem]['hidden']} hidden singles, ",end="")
        print(f"{suSolvedInfo[elem]['loops']} loops",end="")
        print(" ")

        