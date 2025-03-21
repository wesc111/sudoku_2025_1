
# a structure for candidates contain the row, col and the list of possible values
# 
VERSION = "0.21"
VERSION_DATE = "13-Mar-2025"

import copy
class candidate:
    """a canditate is defined as a list for one SUDOKU element that represents all possible values for that element"""
    def __init__(self, row, col, possibleValueList):
        self.row = row
        self.col = col
        self.possibleValueList = possibleValueList

    def __str__(self):
        return f"[{self.row}, {self.col}, {self.possibleValueList}]"
    
    def __len__(self):
        return len(self.possibleValueList)
    
    def getCandidate(self):
        return [self.row, self.col, self.possibleValueList]
    
    def compare(self, candidate):
        """compare the candidate with the self.candidate, 
        Return True if equal, otherwise return False"""
        if candidate.row!=self.row:
            return False
        if candidate.col!=self.col:
            return False
        if candidate.possibleValueList!=self.possibleValueList:
            return False
        return True

    def removeElements(self, valueList):
        """return value: candidate in which all values that are indentical to elements defined in valueList are removed"""
        newPvlList = []
        for elem in self.possibleValueList:
            if (elem not in valueList) and (elem not in newPvlList):
                newPvlList.append(elem)
        return candidate(self.row,self.col,newPvlList)
    
    def removeElementsNotInValueList(self, valueList):
        """return value: candidate in which all values that are not in the value list are removed"""
        newPvlList = []
        for elem in self.possibleValueList:
            if (elem in valueList) and (elem not in newPvlList):
                newPvlList.append(elem)
        return candidate(self.row,self.col,newPvlList)
    
class candidateList:
    """a candidateList is the list of candidates containing candidates (such list can be defined for row, col, box or for the overall sudoku)"""
    """the candidateList should always be sorted"""
    def __init__(self, candidateList, name=""):
        self.candidateList =copy.deepcopy(candidateList)
        #self.sort()
        self.name = name

    def __str__(self):
        """print the content of the candidate list"""
        retStr =  f"{self.name} = "
        if len(self.candidateList)==0:
             retStr = retStr + f"[]"
        else:
            isFirst = True
            for candidate in self.candidateList:
                if isFirst:
                    retStr = retStr + f" {candidate}"
                    isFirst = False
                else:
                    retStr = retStr + f", {candidate}"
        return retStr
    
    def __len__(self):
        return len(self.candidateList)
    
    def __getitem__(self, k):
        len = self.candidateList.__len__()
        if not 0 <= k < len:
            raise IndexError('Index out of range')
        c1 = self.getCandidateList()
        for index, candidate in enumerate(c1):
            if k==index:
                return candidate.getCandidate()
        return 0
    
    def setName(self, name):
        self.name = name

    def getCandidateList(self):
        return self.candidateList
    
    def getSingles(self):
        """return number of singles and all single candidates in the list"""
        retNum=0
        retList=[]
        for index, candidate in enumerate(self.candidateList):
            if candidate!=None:
                if len(candidate)==1:
                    retList.append(candidate)
                    retNum += 1
        return retNum, retList
        
    def getHiddenSingles(self):
        """return number of hidden singles and all hidden single candidates in the list"""
        retNum=0
        retList=[]
        count = [0,0,0,0,0,0,0,0,0,0]
        for index, cc in enumerate(self.candidateList):
            try:    myList = cc.possibleValueList
            except: break
            for elem in cc.possibleValueList:
                count[elem] += 1
        for index, cc in enumerate(self.candidateList):
            try:    myList = cc.possibleValueList
            except: break
            for elem in cc.possibleValueList:
                if count[elem] == 1:
                   hiddenSingleCandidate = candidate(cc.row,cc.col,[elem])
                   retList.append(hiddenSingleCandidate)
                   retNum += 1
        return retNum, retList 
    
    def append(self, operand):
        """append a candidate to the list"""
        self.candidateList.append(operand)
        self.sort()

    def count(self, number):
        """ count how often the number is included in the candidate list"""
        c1 = self.getCandidateList()
        count = 0
        for cc in c1:
            for elem in cc.possibleValueList:
                if elem==number:    count += 1
        return count

    def remove_rc(self, row, col):
        """remove a candidate defined by row, col"""
        for index, elem in enumerate(self.candidateList):
            if elem.row==row and elem.col==col:
                del(self.candidateList[index])

    def remove_pv(self, possibleValueList):
        """remove all candidate that are identical to the possible value list"""
        indexListForRemoval = []
        for index, elem in enumerate(self.candidateList):
            if elem.possibleValueList == possibleValueList:
                indexListForRemoval.append(index)
        for index in sorted(indexListForRemoval, reverse=True):
            del(self.candidateList[index])

    def removeElements(self, valueList):
        """return value: candidate list in which all candidate that are indentical to elements defined in valueList are removed"""
        cl = copy.deepcopy(self)
        retVal = candidateList([],cl.name + "_RE")
        for index, myCandidate in enumerate(cl.candidateList):
            newCandidate=myCandidate.removeElements(valueList)
            retVal.append(newCandidate)
        return retVal
        
    def sort(self):
        """sort the candidate list by row, col"""
        if self.candidateList == None:
            return None
        sortedCandidateList=[]
        for row in range(0,9):
            for col in range(0,9):
                for elem in self.candidateList:
                    if elem!=None:
                        if elem.row==row and elem.col==col:
                            sortedCandidateList.append(elem)
        self.candidateList=sortedCandidateList

    def compare(self, candidateList,debugFlag=0):
        """compare the candidateList with the self.candidateList, 
        Return True if equal, otherwise return False"""
        # first check the length that must be the same
        if len(candidateList)!=len(self.candidateList):
            return False
        # if len is the same, we do a comparison for each element
        c1 = self.getCandidateList()
        c2 = candidateList.getCandidateList()
        for index, elem in enumerate(c1):
            if elem.compare(c2[index])==False:
                if debugFlag>0:     print(f"candidateList.compare() False for element {index}: {c1[index]} != {c2[index]}")
                return False
        return True
    
    def getAllBoxCandidates(self, box):
        """get all candidates for all empty cells in a box"""
        boxRC=[[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]
        retCandidateList = None
        rowi, coli = boxRC[box]
        for row in range(rowi,rowi+3):
            for col in range(coli,coli+3):               
                if self.board[row][col] == 0:
                    myCandidate = self.getCandidate(row,col)
                    if retCandidateList==None:
                        retCandidateList=candidateList([myCandidate],f"CL box[{box}]")
                    else:
                        retCandidateList.append(myCandidate)
        retCandidateList2 = retCandidateList.reduceCandidateListForHiddenPairs(1)                  
        return retCandidateList2

    def getPerm2(self):
        """generate a list of all relevant 2-er permutations of a,b"""
        a=[1,2,3,4,5,6,7,8,9]
        retVal=[]
        for i in range(0,9):
            for j in range(i,9):
                if i!=j:
                    perm = [a[i],a[j]]
                    pp=list(perm)
                    pp.sort()
                    retVal.append(pp)
        return retVal
    
    def countOccurenceInList(self, possibleValueList, number):
        """how often is the number included in the candidateList"""
        count = 0
        for elem in possibleValueList:
            if number in elem:  count += 1
        return count

    def findHiddenPairs(self, debugFlag=0):
        """find hidden pairs: that are pairs that are located inside the candidate list, examples are
           [1,2,3,4], [1,2,6], [3,5], [4,7], [6,9] ... as [1,2] can only be in the first two terms, the list can be reduced to
           [1,2], [1,2], [3,5], [4,7], [6,9] ... note that now 3, 4, and 6 are hidden singles"""
        hiddenPairs=[]
        potentialHiddenPairs=[]
        c1 = self
        if len(c1.candidateList)==0:
            return None
        # to be a hidden pair, both of the perm terms have to be in the same list
        # this is neccessary, but not sufficient
        for perm in self.getPerm2():
            permCount=0
            for elem in c1.candidateList:
                try:
                    pvl = elem.possibleValueList
                except:
                    pvl = None
                    break
                if (perm[0] in pvl) and (perm[1] in pvl):
                    permCount += 1
                if permCount==2 and (perm not in potentialHiddenPairs):
                    potentialHiddenPairs.append(perm)
        if debugFlag>0: print(f"... findHiddenPairs: found potential hidden pairs: {potentialHiddenPairs}")
        # to be truly a hidden pair, the elements found need to have a count of 2, otherwise it's no hidden pair
        for pair in potentialHiddenPairs:
            count1=c1.count(pair[0])
            count2=c1.count(pair[1])
            if count1==2 and count2==2:
                hiddenPairs.append(pair)
        if debugFlag>0: print(f"... findHiddenPairs: found hidden pairs {hiddenPairs}")
        return hiddenPairs
    
    def findPairs(self, debugFlag=0):
        """find (first) pairs in candidate list"""
        count = 0
        for elem in self.candidateList:
            try:
                pvl = elem.possibleValueList
            except:
                pvl = None
                break
            if len(pvl)==2 and count==0:
                firstPair = pvl
                count += 1
            elif len(pvl)==2 and count==1:
                if pvl == firstPair:
                    return pvl
        return None
    
    def findTripples(self, debugFlag=0):
        """find (first) tripple in candidate list"""
        count = 0
        for elem in self.candidateList:
            pvl = elem.possibleValueList
            if len(pvl)==3 and count==0:
                firstTripple = pvl
                count += 1
            elif len(pvl)==3 and count==1:
                if pvl == firstTripple:
                    secondTripple = pvl
                    count += 1
            elif len(pvl)==3 and count==2:
                if pvl == secondTripple:
                    if debugFlag>0: 
                        print(pvl)
                    return pvl
        return None

    def pairs2list(self, pairs):
        """generate a list of numbers that are inside the pairs list"""
        removalList=[]
        for pair in pairs:
            for number in pair:
                if number not in removalList:
                    removalList.append(number)
        return removalList

    def reduceCandidateListForHiddenPairs(self, debugFlag=0):
        """check 2-er permutations that are inside of candidateList: 
        all values beside the 2-er permutation are removed"""
        hiddenPairs = self.findHiddenPairs(0)
        if debugFlag>0 and len(hiddenPairs)>0: print(f"... findHiddenPairs: found hidden pairs {hiddenPairs}")

        removalList = self.pairs2list(hiddenPairs)
        if len(removalList)==0:  # nothing to do here, return the candidate list without changes
            return self
        
        reducedCandidateList = candidateList([], self.name + "_RCL")
        cl = copy.deepcopy(self)
        for index, cc in enumerate(cl.getCandidateList()):
            pvl = cc.possibleValueList
            appendedFlag = False
            pairList = []
            for pair in hiddenPairs:
                if (pair[0] in pvl) or (pair[1] in pvl):
                    pairList.append(pair[0])
                    pairList.append(pair[1])
                    appendedFlag = True
            if appendedFlag:
                reducedCandidateList.append(candidate(cc.row, cc.col, pairList))
            else:
                reducedCandidateList.append(candidate(cc.row, cc.col, pvl))       
 
        return reducedCandidateList
    
    def reduceCandidateListBesidePairs(self, debugFlag=0):
        """if a pair is found, remove elements of that pair in all other candidates of that candidate list"""
        pair = self.findPairs(self.candidateList)
        if pair == None:
            return self
        if debugFlag>0:  print(f"...reduceCandidateListBesidePairs: found pair {pair}")
        reducedCandidateList = candidateList([], self.name + "_RCL2")
        for myCandidate in self.candidateList:
            if myCandidate.possibleValueList == pair:
                reducedCandidateList.append(myCandidate)
            else:
                if pair!=None:
                    modifiedCandidate = myCandidate.removeElements(pair)
                    reducedCandidateList.append(modifiedCandidate)
        return reducedCandidateList
    
    def reduceCandidateListBesideTripples(self, debugFlag=0):
        """if a pair is found, remove elements of that pair in all other candidates of that candidate list"""
        tripple = self.findTripples()
        if tripple == None:
            return self
        if debugFlag>0:  print(f"...reduceCandidateListBesideTripples: found tripple {tripple}")
        reducedCandidateList = candidateList([], self.name + "_RCL3")
        for myCandidate in self.candidateList:
            if myCandidate.possibleValueList == tripple:
                reducedCandidateList.append(myCandidate)
            else:
                if tripple!=None:
                    modifiedCandidate = myCandidate.removeElements(tripple)
                    reducedCandidateList.append(modifiedCandidate)
        return reducedCandidateList
    

