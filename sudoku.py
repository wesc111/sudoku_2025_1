#!/usr/local/bin/python3

""" program to solve SUDOKUs by finding unique candidates
For command description, start $python3 sudoku.py -help
"""

VERSION = "0.1"
VERSION_DATE = "18-Feb-2025"

# file name of input file with SUDOKUs
SU_FILE_NAME = "easy_50.txt"
#SU_FILE_NAME = "sudoku_1.txt"

DEBUG_LEVEL = 0

# select the SUDOKUs to be solved by their number in the file
# for example, to solve SUDOKUs 6,7 and 10, set SU_NUM_LIST = [6,7,10]
SU_NUM_LIST = [22]
# for case that all SUDOKUs in the file should be solved, set SOLVE_ALL = True
# in this case, the list SU_NUM_LIST is ignored
SOLVE_ALL = True

from sudoku_io import sudoku_io

class sudoku():
    """A class to represent a SUDOKU board and to solve it"""

    # max loops for the solver (avoid endless loops)
    MAX_SOLVER_LOOPS = 100

    def __init__(self, board):
        """initialize the SUDOKU board"""
        self.board = board
        self.numUniqueCandidatesFound = 0
        self.numHiddenSinglesFound = 0
        self.loopCount = 0
        self.debugLevel = 0
        self.comment = ""

    def __str__(self):
        """return the SUDOKU in a string format"""
        myStr = ""
        for i in range(0,9):
            if i % 3 == 0:
                myStr += f"+-------+-------+-------+\n"
            # print a line of the SUDOKU
            for j in range(0,9):
                if j % 3 == 0:
                    myStr += "| "
                if self.board[i][j] == 0:
                    myStr += ". "
                else:
                    myStr += f"{self.board[i][j]} "
            myStr += "|\n"
        myStr += f"+-------+-------+-------+"
        return myStr
    
    def getRow(self,row):
        """return all elements of a row"""
        return self.board[row]
    
    def getCol(self,col):
        """return all elements of a column"""
        return [self.board[i][col] for i in range(0,9)]
    
    def getBox(self,row,col):
        """return all elements of a 3x3 box"""
        # do first a floor division, so that any element index in a box can be used to select the corresponding box
        rowi = (row // 3) * 3
        coli = (col // 3) * 3
        box = []
        for i in range(rowi,rowi+3):
            for j in range(coli,coli+3):
                box.append(self.board[i][j])
        return box
    
    def getElem(self,row,col):
        """return the element at a given position"""
        return self.board[row][col]
    
    def setElem(self,row,col,value):
        self.board[row][col] = value

    def setDebugLevel(self,level):
        self.debugLevel = level

    def setComment(self,comment):
        self.comment = comment
    
    def getCandidates(self,row,col):
        """get all candidates at row col (elements not used in a row, column and box)"""
        usedElements = set(self.getRow(row) + self.getCol(col) + self.getBox(row,col))
        if 0 in usedElements:
            usedElements = usedElements - {0}
        # candidates are the elements that are not used, so these are
        # the difference between the set of all elements and the set of used elements
        candidates = set(range(1,10)) - usedElements
        # create a sorted list of candidates as return value
        cl = list(candidates)
        cl.sort()
        return cl
    
    def getCountCandidates(self,candidates):
        count = {i:0 for i in range(1,10)}
        for elemList in candidates:
            for elem in elemList:
                count[elem] += 1
        return count
    
    def findHiddenSinglesInRow(self, row):
        """check for hidden singles in a row"""
        candidates = []
        numHiddenSingles = 0
        for col in range(0,9):
            if self.getElem(row,col) == 0:
                candidates.append(self.getCandidates(row,col))
        if self.debugLevel>0:
            print(f"candidates for row {row}: {candidates}")
        # count each candidate
        count = self.getCountCandidates(candidates)
        # now check for hidden singles (count for a hidden single is 1)
        for i in range(1,10):
            if count[i] == 1: # hidden single found
                numHiddenSingles += 1
                for col in range(0,9):
                    if self.getElem(row,col)==0 and (i in self.getCandidates(row,col)):  # if element is empty and candidate is in the list
                        self.setElem(row,col,i)
                        if self.debugLevel>0:
                            print(f"Hidden single found in row: row={row}, col={col} for elem {i}")
        return numHiddenSingles
    
    def findHiddenSinglesInCol(self, col):
        """check for hidden singles in a column"""
        candidates = []
        numHiddenSingles = 0
        for row in range(0,9):
            if self.getElem(row,col) == 0:
                candidates.append(self.getCandidates(row,col))
        if self.debugLevel>0:
            print(f"candidates for col {col}: {candidates}")
        # count each candidate
        count = self.getCountCandidates(candidates)
        # now check for hidden singles (count for a hidden single is 1)
        for i in range(1,10):
            if count[i] == 1: # hidden single found
                numHiddenSingles += 1
                for row in range(0,9):
                    if self.getElem(row,col)==0 and (i in self.getCandidates(row,col)):  # if element is empty and candidate is in the list
                        self.setElem(row,col,i)
                        if self.debugLevel>0:
                            print(f"Hidden single found in col: row={row}, col={col} for elem {i}")
        return numHiddenSingles
    
    def findHiddenSinglesInBlock(self, block):
        """check for hidden singles in a column"""
        candidates = []
        numHiddenSingles = 0
        rowStart = (block // 3)*3
        colStart = (block % 3)*3
        for rd, cd in [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]:
            row = rowStart + rd
            col = colStart + cd
            if self.getElem(row,col) == 0:
                candidates.append(self.getCandidates(row,col))
        if self.debugLevel>0:
            print(f"candidates for block {block}: {candidates}")
        # count each candidate
        count = self.getCountCandidates(candidates)
        # now check for hidden singles (count for a hidden single is 1)
        for i in range(1,10):
            if count[i] == 1: # hidden single found
                numHiddenSingles += 1
                for rd, cd in [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]:
                    row = rowStart + rd
                    col = colStart + cd
                    if self.getElem(row,col)==0 and (i in self.getCandidates(row,col)):  # if element is empty and candidate is in the list
                        self.setElem(row,col,i)
                        if self.debugLevel>0:
                            print(f"Hidden single found in block: block={block}, row={row}, col={col} for elem {i}")
        return numHiddenSingles

    def findHiddenSingles(self):
        """find all hidden singles in rows, cols and blocks: returns the number of hidden singles found"""
        numHiddenSingles = 0
        for i in range(0,9):
            numHiddenSingles += self.findHiddenSinglesInRow(i)
        self.numHiddenSinglesFound += numHiddenSingles
        for i in range(0,9):
            numHiddenSingles += self.findHiddenSinglesInCol(i)
        self.numHiddenSinglesFound += numHiddenSingles
        for i in range(0,9):
            numHiddenSingles += self.findHiddenSinglesInBlock(i)
        self.numHiddenSinglesFound += numHiddenSingles
        return numHiddenSingles

    def isSolved(self):
        """check if the SUDOKU is solved"""
        for i in range(0,9):
            if 0 in self.getRow(i) or 0 in self.getCol(i):
                return False
        return True
    
    def solve(self):
        """solve the SUDOKU by finding unique candidates"""
        foundUniqueCandidate = True
        foundHiddenSingle = True
        i = 0
        while foundUniqueCandidate or foundHiddenSingle:
            foundUniqueCandidate = False
            foundHiddenSingle = False
            if self.isSolved() or i > self.MAX_SOLVER_LOOPS:
                self.loopCount=i
                break
            if self.debugLevel>0:
                print(f"Loop {i}:")
            for row in range(0,9):
                for col in range(0,9):
                    if self.getElem(row,col) == 0:
                        if len(self.getCandidates(row,col)) == 1:
                            if self.debugLevel>0:
                                print(f"Unique candidate for ({row},{col}): {self.getCandidates(row,col)}")
                            self.numUniqueCandidatesFound += 1
                            foundUniqueCandidate = True
                            self.setElem(row,col,list(self.getCandidates(row,col))[0])
            if not foundUniqueCandidate:
                if self.findHiddenSingles()>0:
                    foundHiddenSingle = True         
            i += 1
            if (foundUniqueCandidate or foundHiddenSingle) and self.debugLevel>0:
                print(s)
        self.loopCount=i

    def printStatistics(self):
        """print statistics of the solution"""
        print(f"Number of unique candidates found: {self.numUniqueCandidatesFound}")
        if self.numHiddenSinglesFound>0:
            print(f"Number of hidden singles found: {self.numHiddenSinglesFound}")
        print(f"Number of loops: {self.loopCount}")
        if s.isSolved():
            print("SUCCESS: SUDOKU is solved")
        else:
            print("FAIL: SUDOKU is not solved")
    # end of class: sudoku

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
            s.setComment(comment)
            s.solve()
            print("\n===== SUDOKU after solving =====")
            print(s)
            s.printStatistics()
            suSolvedInfo[fNum] = {"solved":s.isSolved(), "unique":s.numUniqueCandidatesFound, "hidden":s.numHiddenSinglesFound, "loops":s.loopCount, "comment":s.comment}
        fNum += 1   

    print("\n===== SUMMARY =====")
    for elem in suSolvedInfo:
        print(f"SUDOKU {elem}: {suSolvedInfo[elem]['comment']}")
        print(f"{'   ... SOLVED ' if suSolvedInfo[elem]['solved'] else '   ... NOT SOLVED '}",end="")
        print(f"with {suSolvedInfo[elem]['unique']} unique candidates, ",end="")
        if suSolvedInfo[elem]['hidden']>0:
            print(f"{suSolvedInfo[elem]['hidden']} hidden singles, ",end="")
        print(f"{suSolvedInfo[elem]['loops']} loops",end="")
        print(" ")

        