#!/usr/local/bin/python3

""" program to solve SUDOKUs by finding unique candidates
For command description, start $python3 sudoku.py -help
"""

VERSION = "0.2"
VERSION_DATE = "10-Mar-2025"

# file name of input file with SUDOKUs
SU_FILE_NAME = "easy_50.txt"
# SU_FILE_NAME = "sudoku_1.txt"

# ===== current result for easy_50.txt:
#= Summary: unsolved count = 6
#= Summary:   solved count = 44
#= Summary: 88.0 % of the SUDOKUs are solved
# Average elapsed time per solved SUDOKU [ms]: 8.168
# Average elapsed time per unsolved SUDOKU [ms]: 13.021
# Average elapsed time per SUDOKU [ms]: 8.750

DEBUG_LEVEL = 1

# select the SUDOKUs to be solved by their number in the file
# for example, to solve SUDOKUs 6,7 and 10, set SU_NUM_LIST = [6,7,10]
SU_NUM_LIST = [6]
# for case that all SUDOKUs in the file should be solved, set SOLVE_ALL = True
# in this case, the list SU_NUM_LIST is ignored
SOLVE_ALL = True
# no DEBUG when all SUDOKUs should be solved
if SOLVE_ALL:
    DEBUG_LEVEL = 0

from sudoku_io import sudoku_io
from sudoku_p import sudoku
import time

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
    for index, su in enumerate(suTextList):
        comment = suCommentList[fNum-1]
        if SOLVE_ALL or (fNum in SU_NUM_LIST):
            board =  getBoard(su)
            # create a sudoku object
            if board is None:
                print(f"Error: SUDOKU {fNum} is not valid")
                fNum += 1
                continue
            if not SOLVE_ALL: print("\n")
            print(f"===== SUDOKU: {fNum} ({comment}) =====")
            s = sudoku(board)
            s.setDebugLevel(DEBUG_LEVEL)
            if not SOLVE_ALL: print(s)
            # run the solver
            startTime = time.process_time_ns()
            suIsSolved = s.solve()
            endTime = time.process_time_ns()
            elapsedTime_ms = (endTime - startTime)/1.0e6
            if suIsSolved:
                print(f"PASS, SUDOKU {fNum} ({comment}) is solved")
            else:
                print(f"FAIL, SUDOKU {fNum} ({comment}) could not be solved")
            if not SOLVE_ALL:   print(s)
            else: print(f"Elapsed time [ms]: {elapsedTime_ms:.3f}")
             # for each sudoku some info is stored for summary later on
            suSolvedInfo[fNum] = {"solved":s.isSolved(), "unique":s.numUniqueCandidatesFound, "hidden": s.numHiddenSinglesFound, "loops":s.loopCount, "elapsedTime_ms":elapsedTime_ms, "comment":s.comment}
        fNum += 1

    solvedCount = 0
    notSolvedCount = 0
    solvedList = []
    unsolvedList = []
    totalElapsedTime_ms = 0.0
    totalElapsedTimeSolved_ms = 0.0
    totalElapsedTimeUnsolved_ms = 0.0
    print("\n===== SUMMARY of all SUDOKUs =====")
    for elem in suSolvedInfo:
        print(f"SUDOKU {elem}: {suSolvedInfo[elem]['comment']}",end="")
        totalElapsedTime_ms += suSolvedInfo[elem]["elapsedTime_ms"]
        if suSolvedInfo[elem]['solved']:
            totalElapsedTimeSolved_ms += suSolvedInfo[elem]["elapsedTime_ms"]
            solvedCount += 1
            solvedList.append(elem)
            print(f"   ... SOLVED     #{solvedCount}")
        else:
            totalElapsedTimeUnsolved_ms += suSolvedInfo[elem]["elapsedTime_ms"]
            notSolvedCount += 1
            unsolvedList.append(elem)
            print(f"   ... NOT SOLVED #{notSolvedCount}")
        print(f"with {suSolvedInfo[elem]['unique']} unique candidates, ",end="")
        if suSolvedInfo[elem]['hidden']>0:
            print(f"{suSolvedInfo[elem]['hidden']} hidden singles, ",end="")
        print(f"{suSolvedInfo[elem]['loops']} loops",end="")
        print(" ")

    print(f"===== Total of {solvedCount} SUDOKUs are solved")
    print(f"===== Total of {notSolvedCount} SUDOKUs are not solved")
    print(f"SUDOKUs that are solved: {solvedList}")
    print(f"SUDOKUs that are not solved: {unsolvedList}")
    print(f"= Summary: unsolved count = {notSolvedCount}")
    print(f"= Summary:   solved count = {solvedCount}")
    print(f"= Summary: {100.0 * solvedCount/(solvedCount+notSolvedCount):.1f} % of the SUDOKUs are solved")
    if solvedCount>0:
        print(f"Average elapsed time per solved SUDOKU [ms]: {totalElapsedTimeSolved_ms / (solvedCount):.3f}")
    if notSolvedCount>0:
        print(f"Average elapsed time per unsolved SUDOKU [ms]: {totalElapsedTimeUnsolved_ms / (notSolvedCount):.3f}")
    if (solvedCount + notSolvedCount)>0:
        print(f"Average elapsed time per SUDOKU [ms]: {totalElapsedTime_ms / (solvedCount + notSolvedCount):.3f}")