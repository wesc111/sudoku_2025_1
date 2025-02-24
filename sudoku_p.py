""" class sudoku: this is a class to solve SUDOKU puzzles """

VERSION = "0.1"
VERSION_DATE = "18-Feb-2025"

# a structure for candidates contain the row, col and the list of possible values
class candidate:
    def __init__(self, row, col, candidateList):
        self.row = row
        self.col = col
        self.candidateList = candidateList

    def __str__(self):
        if len(self.candidateList) == 1:
            return f"{self.row},{self.col}: {self.candidateList}        ***"
        else:
            return f"{self.row},{self.col}: {self.candidateList}"

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

    def getAllCandidatesList(self):
        """get all candidates for all empty cells"""
        cl = []
        for row in range(0,9):
            for col in range(0,9):
                if self.board[row][col] == 0:
                    cl.append(candidate(row,col,self.getCandidates(row,col)))
        return cl
    
    def getAllCandidatesList2(self):
        cl = []
        rowColList = []
        for row in range(0,9):
            for col in range(0,9):
                if self.board[row][col] == 0:
                    rowColList.append(candidate(row,col,self.getCandidates(row,col)))
        cl.append(rowColList)
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
                        self.numHiddenSinglesFoundinRow +=1
                        numHiddenSingles += 1
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
                        self.numHiddenSinglesFoundinCol +=1
                        numHiddenSingles += 1
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
                for rd, cd in [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]:
                    row = rowStart + rd
                    col = colStart + cd
                    if self.getElem(row,col)==0 and (i in self.getCandidates(row,col)):  # if element is empty and candidate is in the list
                        self.setElem(row,col,i)
                        self.numHiddenSinglesFoundinBlock +=1
                        numHiddenSingles += 1
                        if self.debugLevel>0:
                            print(f"Hidden single found in block: block={block}, row={row}, col={col} for elem {i}")
        return numHiddenSingles

    def findHiddenSingles(self):
        """find all hidden singles in rows, cols and blocks: returns the number of hidden singles found"""
        numHiddenSingles = 0
        for i in range(0,9):
            numHiddenSingles += self.findHiddenSinglesInRow(i)
        for i in range(0,9):
            numHiddenSingles += self.findHiddenSinglesInCol(i)
        for i in range(0,9):
            numHiddenSingles += self.findHiddenSinglesInBlock(i)
        return numHiddenSingles

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

    def findUniqueCandidates(self):
        """find all unique candidates in the SUDOKU: returns the number of unique candidates found"""
        foundUniqueCandidate = False
        allCandidates = self.getAllCandidatesList()
        self.printAllCandidates(allCandidates)
        for clist in allCandidates:
            if len(clist.candidateList) == 1:
                self.numUniqueCandidatesFound += 1
                foundUniqueCandidate = True
                self.setElem(clist.row,clist.col,clist.candidateList[0])
        return foundUniqueCandidate

    def printAllCandidates(self,allCandidates):
        """print all candidates in the SUDOKU"""
        if self.debugLevel>0:
            print(f"List of all Candidates (unique ones that are used for solving are marked with ***):")
            for c in allCandidates:
                print(f"    {c}")

    def removeNakedTwinsInCandidateList(cl):
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
            candidates = list(elem.candidateList)
            candidates.sort()
            if len(candidates) == 2:
                doubleList.append(candidates)
        for elem in doubleList:  # now, for each element in doubleList, check if it is 2x in list. If yes, add it to listofElementsinSameDoubles
            doubleListWithoutActualElem = doubleList.copy()
            doubleListWithoutActualElem.remove(elem)
            if elem in doubleListWithoutActualElem:
                listofElementsinSameDoubles_1 += elem
        listofElementsinSameDoubles = sorted(list(set(listofElementsinSameDoubles_1)))
        print(f"listofElementsinSameDoubles: {listofElementsinSameDoubles}")
        for myCandidate in cl:
            # don't change items that are 1 elements long and items that are 2 long and in listofElementsinSameDoubles
            if len(myCandidate.candidateList) == 1 or all2ItemsInList(myCandidate.candidateList, listofElementsinSameDoubles): 
                retCandidateList.append(myCandidate)
                continue
            newCandidateList = myCandidate.candidateList.copy()
            for elem in myCandidate.candidateList:
                if elem in listofElementsinSameDoubles:
                    newCandidateList.remove(elem)
            myCandidate.candidateList = newCandidateList
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
            if self.debugLevel>0:
                print(f"Loop {i}:")
            foundUniqueCandidate = self.findUniqueCandidates()
            if not foundUniqueCandidate:
                if self.findHiddenSingles()>0:
                    foundHiddenSingle = True         
            i += 1
            if (foundUniqueCandidate or foundHiddenSingle) and self.debugLevel>0:
                print(self.board)
        self.loopCount=i

    def printStatistics(self):
        """print statistics of the solution"""
        print(f"Number of empty cells in SUDOKU (at start): {self.numEmptyCellsAtStart}")
        print(f"Number of unique candidates found: {self.numUniqueCandidatesFound}")
        print(f"Number of hidden singles found:  {self.numHiddenSinglesFoundinRow} in rows, {self.numHiddenSinglesFoundinCol} in columns, {self.numHiddenSinglesFoundinBlock} in blocks")
        print(f"Number of loops: {self.loopCount}")
        if self.isSolved():
            print("SUCCESS: SUDOKU is solved")
        else:
            print("FAIL: SUDOKU is not solved")
    # end of class: sudoku