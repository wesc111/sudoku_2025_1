

# a structure for candidates contain the row, col and the list of possible values
class candidate:
    def __init__(self, row, col, candidateList):
        self.row = row
        self.col = col
        self.candidateList = candidateList

    def __str__(self):
        return f"Candidates at row={self.row}, col={self.col}: {self.candidateList}"

class sudoku():
    """A class to represent a SUDOKU board and to solve it"""

    def __init__(self, board):
        """initialize the SUDOKU board"""
        self.board = board
        self.numUniqueCandidatesFound = 0
        self.numHiddenSinglesFound = 0
        self.loopCount = 0
        self.debugLevel = 0
        self.comment = ""
        self.numEmptyCellsAtStart = self.getNumEmptyCells()
        self.numHiddenSinglesFoundinRow = 0
        self.numHiddenSinglesFoundinCol = 0
        self.numHiddenSinglesFoundinBlock = 0

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
    
    def getAllCandidatesList(self):
        """get all candidates for all empty cells"""
        cl = []
        for i in range(0,9):
            for j in range(0,9):
                if self.board[i][j] == 0:
                    cl.append(candidate(i,j,self.getCandidates(i,j)))
        return cl
    
    def getNumEmptyCells(self):
        """return the number of empty cells in the SUDOKU"""
        numEmpty = 0
        for i in range(0,9):
            numEmpty += self.getRow(i).count(0)
        return numEmpty

def getCandidates1():
    cl = [[1, 2], [1, 3, 4, 5], [3, 4, 5]]
    return cl

def getCandidates2():
    cl = [ candidate(0,0,[1,2,3,4]), candidate(0,1,[4,5]), candidate(0,2,[1,2,3,4,5]) ]
    return cl

board = [ [0,0,3,0,2,0,6,0,0], 
          [9,0,0,3,0,5,0,0,1],
          [0,0,1,8,0,6,4,0,0],
          [0,0,8,1,0,2,9,0,0],
          [7,0,0,0,0,0,0,0,8],
          [0,0,6,7,0,8,2,0,0],
          [0,0,2,6,0,9,5,0,0],
          [8,0,0,2,0,3,0,0,9],
          [0,0,5,0,1,0,3,0,0] ]

s = sudoku(board)
print(s)
allCandidates = s.getAllCandidatesList()
print("\nAll candidates:")
for c in allCandidates:
    print(c)
