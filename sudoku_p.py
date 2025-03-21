

""" class sudoku: this is a class to solve SUDOKU puzzles """

from candidate_p import candidate
from candidate_p import candidateList
import copy
import random

# works with standard python lists, no specific need for any additional packages

VERSION = "0.21"
VERSION_DATE = "13-Mar-2025"

# the main SUDOKU class
class sudoku():
    """A class to represent a SUDOKU board and to solve it"""

    # max loops for the solver (avoid endless loops)
    MAX_SOLVER_LOOPS = 100
    # select removal of naked twins in candidate lists, should always be set to TRUE
    REMOVE_NAKED_TWINS_IN_CANDIDATE_LIST = True

    FIND_HIDDEN_PAIRS_ENABLED = True
    FIND_PAIRS_ENABLED = True
    FIND_TRIPPLES_ENABLED = True

    MAX_NUM_RAND_TRIALS = 400

    def __init__(self, board):
        """initialize the SUDOKU board"""
        self.board = board
        self.stoBoard = board
        self.debugLevel = 0
        self.comment = ""
        self.numEmptyCellsAtStart = self.getNumEmptyCells()
        self.randCount = 0
        self.loopCount = 0
        self.numUniqueCandidatesFound = 0
        self.numHiddenSinglesFound = 0

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

    def getCandidate(self, row, col):
        """get all candidates at row col (elements not used in a row, column and box)"""
        try:
            usedElements = set(self.getRow(row) + self.getCol(col) + self.getBox(row,col))
        except:
            return None
        if 0 in usedElements:
            usedElements = usedElements - {0}
        # candidates are the elements that are not used, so these are
        # the difference between the set of all elements and the set of used elements
        possibleValues = set(range(1,10)) - usedElements
        # create a sorted list of candidates as return value
        cl = list(possibleValues)
        cl.sort()
        retCandidate = candidate(row, col, cl)
        return retCandidate

    def reduceCandidateList(self, inCandidateList):
        """  function to reduce candidate list by algorithms for doubles, tripples, hidden doubles
             used by getAllRowCandidates(), getAllColCandidates(), getAllBoxCandidates()       
        """
        if inCandidateList==None:                  # nothing to do, there are no candidates here
            return inCandidateList
        hiddenPairs = inCandidateList.findHiddenPairs()
        pairs = inCandidateList.findPairs()
        if len(hiddenPairs)==0 and pairs==None:   # nothing to do, no pairs or hidden pairs, return immediately
            return inCandidateList
        else:
            if self.FIND_HIDDEN_PAIRS_ENABLED:
                retCandidateList1 = inCandidateList.reduceCandidateListForHiddenPairs(self.debugLevel)
            else:
                retCandidateList1 = inCandidateList
            if self.FIND_PAIRS_ENABLED:
                retCandidateList2 = retCandidateList1.reduceCandidateListBesidePairs(self.debugLevel)
            else:
                retCandidateList2 = retCandidateList1
            if self.FIND_TRIPPLES_ENABLED:
                retCandidateList3  = retCandidateList2.reduceCandidateListBesideTripples(self.debugLevel)
            else:
                retCandidateList3 = retCandidateList2
            self.myPrint(f"--> {inCandidateList}")
            self.myPrint(f"--> {retCandidateList3}")
            return retCandidateList3
        
    def getAllRowCandidates(self, row):
        """get all candidates for all empty cells in a row"""
        retCandidateList = None
        for col in range(0,9):
            if self.board[row][col] == 0:
                try:
                    myCandidate = self.getCandidate(row,col)
                except:
                    myCandidate = None
                if retCandidateList==None:
                    retCandidateList=candidateList([myCandidate],f"CL row[{row}]")
                elif myCandidate!=None:
                    retCandidateList.append(myCandidate)
        rtv = self.reduceCandidateList(retCandidateList)
        return rtv
    
    def getAllColCandidates(self, col):
        """get all candidates for all empty cells in a col"""
        retCandidateList = None
        for row in range(0,9):
            if self.board[row][col] == 0:
                try:
                    myCandidate = self.getCandidate(row,col)
                except:
                    myCandidate = None
                if retCandidateList==None:
                    retCandidateList=candidateList([myCandidate],f"CL col[{col}]")
                elif myCandidate!=None:
                    retCandidateList.append(myCandidate)
        rtv = self.reduceCandidateList(retCandidateList)
        return rtv

    def getAllBoxCandidates(self, box):
        """get all candidates for all empty cells in a box"""
        boxRC=[[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]
        retCandidateList = None
        rowi, coli = boxRC[box]
        for row in range(rowi,rowi+3):
            for col in range(coli,coli+3):               
                if self.board[row][col] == 0:
                    try:
                        myCandidate = self.getCandidate(row,col)
                    except:
                        myCandidate = None
                    if retCandidateList==None:
                        retCandidateList=candidateList([myCandidate],f"CL box[{box}]")
                    elif myCandidate!=None:
                        retCandidateList.append(myCandidate)    
        rtv = self.reduceCandidateList(retCandidateList)
        return rtv
    
    def getAllPairCandidates(self):
        pairList=[]
        for row in range(0,9):
            cl = self.getAllRowCandidates(row)
            if cl!=None:
                for elem in cl.candidateList:
                    pvl = elem.possibleValueList
                    if len(pvl)==2:
                        pairList.append(elem)
        return pairList

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

    def printAllCandidates(self):
        """print candidates for the overall sudoku (for all rows)"""
        for row in range(0,9):
            rowCandidateList = self.getAllRowCandidates(row)
            print(rowCandidateList)
            numSingles, rowSingles = rowCandidateList.getSingles()
            if numSingles>0:
                for single in rowSingles:
                    print(f"Found Single: {single}")
            numHiddenSingles, aHiddenSingles = rowCandidateList.getHiddenSingles()
            if numHiddenSingles>0:
                for hiddenSingle in aHiddenSingles:
                    print(f"Found hidden Single: {hiddenSingle}")

    def solvePrintHeader(self, type):
        if type==0:
            self.myPrint(f"== starting solver based on row Candidates")
        elif type==1:
            self.myPrint(f"== starting solver based on col Candidates")
        elif type==2:
            self.myPrint(f"== starting solver based on box Candidates")

    def solve(self):
        """solve SUDOKU """
        foundNewCandidate = True
        i = 0
        while foundNewCandidate:
            foundNewCandidate = False
            self.loopCount = i
            if self.isSolved():                 return True
            elif i > self.MAX_SOLVER_LOOPS:     return False                
            self.myPrint(f"===== Loop {i}:")
            for type in range(0,3):   # loop to run algo on row, col and box candidate lists
                self.solvePrintHeader(type)
                for n in range(0,9):
                    if   type==0:   aCandidateList = self.getAllRowCandidates(n)
                    elif type==1:   aCandidateList = self.getAllColCandidates(n)
                    elif type==2:   aCandidateList = self.getAllBoxCandidates(n)
                    if aCandidateList != None:
                        self.myPrint(aCandidateList)
                        numSingles, aSinges = aCandidateList.getSingles()
                        if numSingles>0:
                            for single in aSinges:
                                self.myPrint(f"... found single: {single}")
                                self.setElem(single.row,single.col,single.possibleValueList[0])
                                self.numUniqueCandidatesFound += 1
                                foundNewCandidate = True                        
                        numHiddenSingles, aHiddenSingles = aCandidateList.getHiddenSingles()
                        if numHiddenSingles>0:
                            for hiddenSingle in aHiddenSingles:
                                self.myPrint(f"... found hidden single: {hiddenSingle}")
                                self.setElem(hiddenSingle.row,hiddenSingle.col,hiddenSingle.possibleValueList[0])
                                self.numHiddenSinglesFound += 1
                                foundNewCandidate = True
            i += 1
        return False
    
    def storeBoard(self):
        """STORE the actual board in stoBoard"""
        for elem in self.board:
            self.stoBoard = copy.deepcopy(self.board)

    def recallBoard(self):
        """RECALL the actual board from stoBoard"""
        for elem in self.board:
            self.board = copy.deepcopy(self.stoBoard)

    def solveRand(self):
        """solve SUDOKU, in case that no analytic solution is found start randomized trials"""
        if self.solve():
            return True
        else:
            print("... no analytic solution found, randomized trials will start here")
            self.storeBoard()
            stored_loopCount = self.loopCount
            stored_numUniqueCandidatesFound = self.numUniqueCandidatesFound
            stored_numHiddenSinglesFound = self.numHiddenSinglesFound
            pairList = self.getAllPairCandidates()
            for i in range(0,self.MAX_NUM_RAND_TRIALS):
                self.randCount += 1
                randPairList =copy.deepcopy(pairList)
                self.myPrint(f"... found {len(pairList)} pairs")
                randPairFlag = []
                # for each pair, generate a rand flag that determines if this element is randomized
                for i, pair in enumerate(pairList):
                    randPairFlag.append(random.randint(0,1))
                # do the randomization and print the randomization
                for i, elem in enumerate(randPairList):
                    if randPairFlag[i]==1:
                        if random.randint(0,1)==1:
                            pvlValue = elem.possibleValueList[1]
                        else:
                            pvlValue = elem.possibleValueList[0]
                        elem.possibleValueList = [pvlValue]
                        self.myPrint(f"{pairList[i]} -> set to {randPairList[i]}")
                # now set the randomized elements
                for i, elem in  enumerate(randPairList):
                    if randPairFlag[i]==1:
                        self.setElem(elem.row, elem.col, elem.possibleValueList[0])
                if self.solve():
                    return True
                # randomization failed here, restore board and statistics before trying the next randomization inside the loop
                self.recallBoard()
                self.loopCount = stored_loopCount
                self.numUniqueCandidatesFound = stored_numUniqueCandidatesFound
                self.numHiddenSinglesFound = stored_numHiddenSinglesFound

            return False

    def printStatistics(self):
        # TBD WSC
        return False  

    # end of class: sudoku