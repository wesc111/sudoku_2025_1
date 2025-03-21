# /usr/local/bin/python3

""" program to solve SUDOKUs by finding unique candidates
For command description, start $python3 sudoku.py -help
"""

VERSION = "0.21"
VERSION_DATE = "13-Mar-2025"

# file name of input file with SUDOKUs
SU_FILE_NAME = "easy_50.txt"
# select the SUDOKUs to be solved by their number in the file
# for example, to solve SUDOKUs 6,7 and 10, set SU_NUM_LIST = [6,7,10]
SU_NUM_LIST = [1]
# for case that all SUDOKUs in the file should be solved, set SOLVE_ALL = True
# in this case, the list SU_NUM_LIST is ignored
SOLVE_ALL = False

# select debug level 
DEBUG_LEVEL = 0

from sudoku_io import sudoku_io
from sudoku_p import sudoku
import time
import sys

# parse input arguments
# example usage: $python sudoku_ex1.py -num=4
if len(sys.argv)>=2:
    for i in range(1,len(sys.argv)):
        actArg = sys.argv[i]
        if "-debug" in actArg:
            DEBUG_LEVEL=1
        if DEBUG_LEVEL>0:
            print(f"... processing argument: {actArg}")
        if "-f" in actArg:
            fname = sys.argv[i+1]
            if len(fname)>0:
                 SU_FILE_NAME=fname
                 print(f"... input file name: {SU_FILE_NAME}")
        if "-num" in actArg:
            n = int(sys.argv[i+1])
            if n<1:
                n=1
            SU_NUM_LIST = [n]
        if "-all" in actArg:
            SOLVE_ALL=True
        if "-noprint" in actArg:
            PRINT_FLAG=False
        if "-h" in actArg:
            print("Optional arguments for sudoku_ex1:")
            print("    -h               ... print help")
            print("    -v               ... show program version")
            print("    -debug           ... show detailed debug info")
            print("    -num 2           ... solve SUDOKU #3")
            print("    -all             ... solve all SUDOKUs read from input file")
            print("    -noprint         ... no print of SUDOKU solution, just print PASS/FAIL results")
            print("    -f sudoku_1.txt  ... read SUDOKUs from file sudoku_1.txt")
            sys.exit()
        if "-v" in actArg:
            print(f"    Welcome to sudoku, this is program version {VERSION} from {VERSION_DATE}")
            sys.exit()

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
   
    numRead = myIo.readFile(SU_FILE_NAME)
    print(f"... total of {numRead} lines read from file name {SU_FILE_NAME}")
 
    # correct numbers above the number of sudokus defined in file
    for i, elem in enumerate(SU_NUM_LIST):
        if SU_NUM_LIST[i]>numRead:
            SU_NUM_LIST[i]=numRead

    suTextList, suCommentList = myIo.getSudokuList()
    # number of the SUDOKU that should be solved
    suNumber = 1
    # loop over all SUDOKUs
    for index, su in enumerate(suTextList):
        comment = suCommentList[suNumber-1]
        # if not all sudokus should be solved, execute only number defined in SU_NUM_LIST
        if not SOLVE_ALL and not (suNumber in SU_NUM_LIST):
            suNumber += 1
            continue
        board =  getBoard(su)
        # create a sudoku object
        if board is None:
            print(f"Error: SUDOKU {suNumber} is not valid")
            suNumber += 1
            continue
        print("\n")
        print(f"===== SUDOKU: {suNumber} ({comment}) =====")
        s = sudoku(board)
        s.setDebugLevel(DEBUG_LEVEL)
        print(s)
        # run the solver
        startTime = time.process_time_ns()
        # -----> HERE THE solver is started <-----
        suIsSolved = s.solveRand()
        endTime = time.process_time_ns()
        elapsedTime_ms = (endTime - startTime)/1.0e6
        if suIsSolved:
            print(f"PASS, SUDOKU {suNumber} ({comment}) is solved")
        else:
            print(f"FAIL, SUDOKU {suNumber} ({comment}) could not be solved")
        print(s)
        print(f"Elapsed time [ms]: {elapsedTime_ms:.3f}")
            # for each sudoku some info is stored for summary later on
        suSolvedInfo[suNumber] = {"solved":s.isSolved(), "unique":s.numUniqueCandidatesFound, "hidden": s.numHiddenSinglesFound, \
                                "loops":s.loopCount, "elapsedTime_ms":elapsedTime_ms, "comment":s.comment, "randCount":s.randCount}
        suNumber += 1

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
        if suSolvedInfo[elem]['randCount']>0:
             print(f"{suSolvedInfo[elem]['randCount']} randomizations, ",end="")
        print(f"{suSolvedInfo[elem]['loops']} loops",end="")
        print(" ")

    print(f"========== Summary for file {SU_FILE_NAME} ==========")
    print(f"===== Total of {solvedCount} SUDOKUs are solved")
    print(f"===== Total of {notSolvedCount} SUDOKUs are not solved")
    if len(unsolvedList)>0:
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