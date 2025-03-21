

""" class sudoku: this is a class to solve SUDOKU puzzles """

from candidate_p import candidate

# works with standard python lists, no specific need for any additional packages

VERSION = "0.2"
VERSION_DATE = "24-Feb-2025"

# the main SUDOKU class
class sudoku():
    """A class to represent a SUDOKU board and to solve it"""

    # max loops for the solver (avoid endless loops)
    MAX_SOLVER_LOOPS = 100
    # select removal of naked twins in candidate lists, should always be set to TRUE
    REMOVE_NAKED_TWINS_IN_CANDIDATE_LIST = True

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
    
    def setDebugLevel(self, level):
        """set the debug level 
        (0 ... no additional printouts, 1 ... do debug printing, >1 ... reserved for future use)"""
        self.debugLevel = level
    def myPrint(self, str, end="\n"):
        """internal print function used in class itself, does the print based on the debug level """
        if self.debugLevel>0:
            print(str,end=end)   
    
    def getRow(self, row):
        """return all elements of a row"""
        return self.board[row]
    
    def getCol(self, col):
        """return all elements of a column"""
        return [self.board[i][col] for i in range(0,9)]
    
    def getBox(self, row, col):
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
    
    def setElem(self, row, col, value):
        """set the element at row, col to value"""
        self.board[row][col] = value

    def setComment(self, comment):
        """set a comment (e.g. for easy identification of the actual SUDOKU) """
        self.comment = comment

    def getCandidates(self, row, col):
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
        if self.REMOVE_NAKED_TWINS_IN_CANDIDATE_LIST:
            retList2 = self.removeNakedTwinsInCandidateList(retList)
        else:
            retList2 = retList
        return retList2

    def getAllColCandidates(self, col):
        """get all candidates for all empty cells in a col"""
        retList = []
        for row in range(0,9):
            if self.board[row][col] == 0:
                retList.append(candidate(row,col,self.getCandidates(row,col)))
        if self.REMOVE_NAKED_TWINS_IN_CANDIDATE_LIST:
            retList2 = self.removeNakedTwinsInCandidateList(retList)
        else:
            retList2 = retList
        return retList2
   
    def getAllBoxCandidates(self, box):
        """get all candidates for all empty cells in a box"""
        boxRC=[[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]
        retList = []
        rowi, coli = boxRC[box]
        for row in range(rowi,rowi+3):
            for col in range(coli,coli+3):
                if self.board[row][col] == 0:
                    retList.append(candidate(row,col,self.getCandidates(row,col)))
        if self.REMOVE_NAKED_TWINS_IN_CANDIDATE_LIST:
            retList2 = self.removeNakedTwinsInCandidateList(retList)
        else:
            retList2 = retList
        return retList2
    
    def getCountCandidates(self, candidateList):
        """for each possible candidate 1 ... 9, count the number of occurances """
        count = {i:0 for i in range(1,10)}
        for candidate in candidateList:
            possibleList = candidate.possibleValueList
            for elem in possibleList:
                count[elem] += 1
        return count

    def isSolved(self):
        """check if the SUDOKU is solved"""
        for i in range(0,9):    # check that there are no empty cells in the board
            if 0 in self.getRow(i):
                return False
        return True
    
    def getNumEmptyCells(self):
        """return the number of empty cells in the SUDOKU"""
        numEmpty = 0
        for i in range(0,9):
            numEmpty += self.getRow(i).count(0)
        return numEmpty

    def print1(self, type, num, list):   # print routine used inside loop of printAllCandidates
        """print1 is used inside printing of candidate lists"""
        if len(list)>0:
            self.myPrint(f"{type} = {num}: ", end="")
            last = list[-1]
            for elem in list:
                if elem!=last:
                    self.myPrint(f"{elem}, ", end="")
                else:
                    self.myPrint(f"{elem}""")

    def findUniqueCandidates(self, type):
        """find all unique candidates in the SUDOKU: returns the number of unique candidates found"""
        foundUniqueCandidate = False
        for n in range(0,9):
            isPrintedFlag = False
            if type=="row":
                candidates = self.getAllRowCandidates(n)
            elif type=="col":
                candidates = self.getAllColCandidates(n)
            elif type=="box":
                candidates = self.getAllBoxCandidates(n)
            if self.REMOVE_NAKED_TWINS_IN_CANDIDATE_LIST:
                candidates2 = self.removeNakedTwinsInCandidateList(candidates)
            else:
                candidates2 = candidates
            for clist in candidates2:
                if len(clist.possibleValueList) == 1:
                    self.numUniqueCandidatesFound += 1
                    foundUniqueCandidate = True
                    if not isPrintedFlag:
                        self.print1(type,n,candidates)
                        isPrintedFlag = True
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

    def removeHiddenSinglesInRCB(self, type):
        """check for hidden singles in a row/col/box and remove it in candidate list"""
        numHiddenSingles = 0
        for n in range(0,9):
            if type=="row":
                cl1 = self.getAllRowCandidates(n)
            elif type=="col":
                cl1 = self.getAllColCandidates(n)
            elif type=="box":
                cl1 = self.getAllBoxCandidates(n)
            # count each candidate
            count = self.getCountCandidates(cl1)
            # now check for hidden singles (count for a hidden single is 1)
            for i in range(1,10):
                if count[i] == 1:
                    hiddenSingle = i   # hidden single found for i
                    numHiddenSingles += 1
                    for candidate in cl1:
                        if hiddenSingle in candidate.possibleValueList:
                            self.setElem(candidate.row, candidate.col, hiddenSingle)
                            if type=="row":     self.numHiddenSinglesFoundinRow += 1
                            elif type=="col":   self.numHiddenSinglesFoundinCol += 1
                            elif type=="box":   self.numHiddenSinglesFoundinBox += 1                           
                            numHiddenSingles += 1
                            self.myPrint(f"Hidden single {hiddenSingle} found in {type} at row={candidate.row}, col={candidate.col}")
                            break
        return numHiddenSingles


    def all2ItemsInList(self, listWith2Elements, listofElementsinSameDoubles):
        """function to check if there are 2 elements in listWith2Elements and if these two elements are included in listofElementsinSameDoubles"""
        if len(listWith2Elements) != 2:
            return False
        for elem in listWith2Elements:
            if elem not in listofElementsinSameDoubles:
                return False
        return True
    
    def removeNakedTwinsInCandidateList(self, myCandidateList):
        """function to find same doubles in a candidate list cl"""
        doubleList = []          # list to store all lists with 2 elements
        listofElementsinSameDoubles_1 = []
        retCandidateList = []    # the return value: a list of candidates with removed elemenbts
        for elem in myCandidateList:     # find all doubles and store elements of doubles in doubleList
            possibleValueList = list(elem.possibleValueList)
            possibleValueList.sort()
            if len(possibleValueList) == 2:
                doubleList.append(possibleValueList)
        for elem in doubleList:  # now, for each element in doubleList, check if it is 2x in list. If yes, add it to listofElementsinSameDoubles
            doubleListWithoutActualElem = doubleList.copy()
            doubleListWithoutActualElem.remove(elem)
            if elem in doubleListWithoutActualElem:
                listofElementsinSameDoubles_1 += elem
        listofElementsinSameDoubles = sorted(list(set(listofElementsinSameDoubles_1)))
        if len(listofElementsinSameDoubles)>0:
            self.myPrint(f"listofElementsinSameDoubles: {listofElementsinSameDoubles}")
        for myCandidate in myCandidateList:
            # don't change items that are 1 elements long and items that are 2 long and in listofElementsinSameDoubles
            if len(myCandidate.possibleValueList) == 1 or self.all2ItemsInList(myCandidate.possibleValueList, listofElementsinSameDoubles): 
                retCandidateList.append(myCandidate)
                continue
            newpossibleValueList = myCandidate.possibleValueList.copy()
            for elem in myCandidate.possibleValueList:
                if elem in listofElementsinSameDoubles:
                    newpossibleValueList.remove(elem)
                    self.myPrint(f"Removed possible value in candidate list of {myCandidate.row},{myCandidate.col}]")
            myCandidate.possibleValueList = newpossibleValueList
            retCandidateList.append(myCandidate)
        return retCandidateList

    def solve(self):
        """solve the SUDOKU by finding unique candidates and/or hidden singles"""
        foundUniqueCandidate = True
        foundHiddenSingle = False
        i = 0
        while foundUniqueCandidate or foundHiddenSingle:
            foundUniqueCandidate = False
            foundHiddenSingle = False
            if self.isSolved() or i > self.MAX_SOLVER_LOOPS:
                self.loopCount=i
                break
            self.myPrint(f"===== Loop {i}:")
            foundUniqueCandidate = self.findUniqueCandidates("row") | self.findUniqueCandidates("col") | self.findUniqueCandidates("box")
            # put priority on unique candidate: only if no unique candidate is found, hidden singles in row/col or box are taken for solving the SUDOKU
            if not foundUniqueCandidate:  
                if self.removeHiddenSinglesInRCB("row")>0:
                    foundHiddenSingle = True  
                if self.removeHiddenSinglesInRCB("col")>0:
                    foundHiddenSingle = True
                if self.removeHiddenSinglesInRCB("box")>0:
                    foundHiddenSingle = True  
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