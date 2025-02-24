""" class sudoku: this is a class to solve SUDOKU puzzles """

VERSION = "0.1"
VERSION_DATE = "18-Feb-2025"

# a structure for candidates contain the row, col and the list of possible values
class candidate:
    def __init__(self, row, col, possibleValueList):
        self.row = row
        self.col = col
        self.possibleValueList = possibleValueList

    def __str__(self):
        return f"[{self.row},{self.col}: {self.possibleValueList}]"

# the main SUDOKU class
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
        self.numEmptyCellsAtStart = self.getNumEmptyCells()
        self.numHiddenSinglesFoundinRow = 0
        self.numHiddenSinglesFoundinCol = 0
        self.numHiddenSinglesFoundinBox = 0

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
    
    def myPrint(self,str,end="\n"):
        """my print function: this is only executed, if debugLevel ist set to a value >0 """
        if self.debugLevel>0:
            print(str,end=end)   
    
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

    def getAllRowCandidates(self, row):
        """get all candidates for all empty cells in a row"""
        retList = []
        for col in range(0,9):
            if self.board[row][col] == 0:
                retList.append(candidate(row,col,self.getCandidates(row,col)))
        return retList

    def getAllColCandidates(self, col):
        """get all candidates for all empty cells in a col"""
        retList = []
        for row in range(0,9):
            if self.board[row][col] == 0:
                retList.append(candidate(row,col,self.getCandidates(row,col)))
        return retList
   
    def getAllBoxCandidates(self, box):
        """get all candidates for all empty cells in a box"""
        boxRC=[[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]
        retList = []
        rowi, coli = boxRC[box]
        for row in range(rowi,rowi+3):
            for col in range(coli,coli+3):
                if self.board[row][col] == 0:
                    retList.append(candidate(row,col,self.getCandidates(row,col)))
        return retList

    def getAllCandidatesList(self):
        """get all candidates for all empty cells in overall board"""
        retList = []
        for row in range(0,9):
            for col in range(0,9):
                if self.board[row][col] == 0:
                    retList.append(candidate(row,col,self.getCandidates(row,col)))
        return retList
    
    def getCountCandidates(self, candidates):
        count = {i:0 for i in range(1,10)}
        for elemList in candidates:
            for elem in elemList:
                count[elem] += 1
        return count

    def isSolved(self):
        """check if the SUDOKU is solved"""
        for i in range(0,9):    # check that there are no empty cells in all rows
            if 0 in self.getRow(i):
                return False
        return True
    
    def getNumEmptyCells(self):
        """return the number of empty cells in the SUDOKU"""
        numEmpty = 0
        for i in range(0,9):
            numEmpty += self.getRow(i).count(0)
        return numEmpty

    def print1(self,type,num,list):   # print routine used inside loop of printAllCandidates
        if len(list)>0:
            self.myPrint(f"{type} = {num}: ", end="")
            last = list[-1]
            for elem in list:
                if elem!=last:
                    self.myPrint(f"{elem}, ", end="")
                else:
                    self.myPrint(f"{elem}""")

    def findUniqueCandidates(self):
        """find all unique candidates in the SUDOKU: returns the number of unique candidates found"""
        foundUniqueCandidate = False
        for row in range(0,9):
            candidatesForRow = self.getAllRowCandidates(row)
            self.print1("Row",row,candidatesForRow)
            for clist in candidatesForRow:
                if len(clist.possibleValueList) == 1:
                    self.numUniqueCandidatesFound += 1
                    foundUniqueCandidate = True
                    self.myPrint(f"Found unique candidate {clist.possibleValueList[0]} at {clist.row},{clist.col}")
                    self.setElem(clist.row,clist.col,clist.possibleValueList[0])
        return foundUniqueCandidate               

    def printAllCandidates(self):
        """print all candidates in the SUDOKU"""
        # for c in allCandidates:
        for n in range(0,9):
            cl1 = self.getAllRowCandidates(n)
            self.print1("Row",n,cl1)
        for n in range(0,9):
            cl2 = self.getAllColCandidates(n)
            self.print1("Col",n,cl2)
        for n in range(0,9):
            cl3 = self.getAllBoxCandidates(n)
            self.print1("Box",n,cl3)


    def removeNakedTwinsInCandidateList(self,cl):
        """function to find same doubles in a candidate list cl"""
        def all2ItemsInList(listWith2Elements, listofElementsinSameDoubles):
            """function to check if there are 2 elements in listWith2Elements and if these two elements are included in listofElementsinSameDoubles"""
            if len(listWith2Elements) != 2:
                return False
            for elem in listWith2Elements:
                if elem not in listofElementsinSameDoubles:
                    return False
            return True
        doubleList = []          # list to store all lists with 2 elements
        listofElementsinSameDoubles_1 = []
        retCandidateList = []    # the return value: a list of candidates with removed elemenbts
        for elem in cl:          # find all doubles and store elements of doubles in doubleList
            candidates = list(elem.possibleValueList)
            candidates.sort()
            if len(candidates) == 2:
                doubleList.append(candidates)
        for elem in doubleList:  # now, for each element in doubleList, check if it is 2x in list. If yes, add it to listofElementsinSameDoubles
            doubleListWithoutActualElem = doubleList.copy()
            doubleListWithoutActualElem.remove(elem)
            if elem in doubleListWithoutActualElem:
                listofElementsinSameDoubles_1 += elem
        listofElementsinSameDoubles = sorted(list(set(listofElementsinSameDoubles_1)))
        self.myPrint(f"listofElementsinSameDoubles: {listofElementsinSameDoubles}")
        for myCandidate in cl:
            # don't change items that are 1 elements long and items that are 2 long and in listofElementsinSameDoubles
            if len(myCandidate.possibleValueList) == 1 or all2ItemsInList(myCandidate.possibleValueList, listofElementsinSameDoubles): 
                retCandidateList.append(myCandidate)
                continue
            newpossibleValueList = myCandidate.possibleValueList.copy()
            for elem in myCandidate.possibleValueList:
                if elem in listofElementsinSameDoubles:
                    newpossibleValueList.remove(elem)
            myCandidate.possibleValueList = newpossibleValueList
            retCandidateList.append(myCandidate)
        return retCandidateList

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
            self.myPrint(f"===== Loop {i}:")
            foundUniqueCandidate = self.findUniqueCandidates()
            #if not foundUniqueCandidate:
            #    if self.findHiddenSingles()>0:
            #        foundHiddenSingle = True         
            i += 1
        self.loopCount=i

    def printStatistics(self):
        """print statistics of the solution"""
        print(f"Number of empty cells in SUDOKU (at start): {self.numEmptyCellsAtStart}")
        print(f"Number of unique candidates found: {self.numUniqueCandidatesFound}")
        print(f"Number of hidden singles found:  {self.numHiddenSinglesFoundinRow} in rows, ",end="") 
        print(f"{self.numHiddenSinglesFoundinCol} in columns, {self.numHiddenSinglesFoundinBox} in boxes")
        print(f"Number of loops: {self.loopCount}")
        if self.isSolved():
            print("SUCCESS: SUDOKU is solved")
        else:
            print("FAIL: SUDOKU is not solved")
    # end of class: sudoku