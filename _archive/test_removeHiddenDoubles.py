
"""test_removeHiddenDoubles.py"""

from candidate_p import candidate
from candidate_p import candidateList

import copy

def getPerm2():
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

def getPerm2Hit(candidateList):
    """check 2-er permutations that are inside of candidateList: 
    if a 2-er permutation is included exactly 2 times, the value is added to the return list retVal"""
    retVal=[]
    allPermList = getPerm2()
    for perm in allPermList:
        count = 0
        for cc in candidateList:
            if (perm[0] in cc) and (perm[1] in cc):
                count += 1
        if count==2 and countOccurenceInList(candidateList,perm[0])==2 and countOccurenceInList(candidateList,perm[1])==2:
            retVal.append(perm)
    return retVal

def countOccurenceInList(candidateList, number):
    """how often is the number included in the candidateList"""
    count = 0
    for elem in candidateList:
        if number in elem:  count += 1
    return count

def getReducedCandidateList_old(candidateList, debugLevel=0):
    hiddenPairList = getPerm2Hit(candidateList)
    if len(hiddenPairList)>0:   # found a hidden pair -> candidate list can be reduced
        if debugLevel>0:    print(f"getReducedCandidateList: found hidden pair {hiddenPairList}")
        retVal = []
        for elem in candidateList:
            elem2=[]
            for hpelem in hiddenPairList:
                for n in elem:
                    if (n!=hpelem[0]) and (n!=hpelem[1]):
                        elem2.append(n)
                retVal.append(elem2)
    else:                       # found no hidden pair, candidate list stays as it is
        if debugLevel>0:    print(f"getReducedCandidateList: No hidden pair found")
        retVal = candidateList
    return retVal

def getReducedCandidateList(candidateList, debugLevel=0):
    retVal = candidateList
    hiddenPairList = getPerm2Hit(candidateList)
    if len(hiddenPairList)>0:   # found hidden pair(s) -> candidate list can be reduced
        if debugLevel>0:    print(f"getReducedCandidateList: found hidden pair {hiddenPairList}")
        for hpelem in hiddenPairList:
            for index, candidate in enumerate(retVal):
                if (hpelem[0] in candidate):
                    retVal[index].remove(hpelem[0])
                if (hpelem[1] in candidate):
                    retVal[index].remove(hpelem[1])
    return retVal

def getReducedCandidateList2(candidateList, debugLevel=0):
    retVal = candidateList
    possibleValueList = []
    for elem in candidateList:
        possibleValueList.append(elem.possibleValueList)
    print("----->",possibleValueList)
    hiddenPairList = getPerm2Hit(possibleValueList)
    if len(hiddenPairList)>0:   # found hidden pair(s) -> candidate list can be reduced
        if debugLevel>0:    print(f"getReducedCandidateList: found hidden pair {hiddenPairList}")
        for hpelem in hiddenPairList:
            for index, candidate in enumerate(retVal):
                if (hpelem[0] in candidate.possibleValueList):
                    retVal[index].possibleValueList.remove(hpelem[0])
                if (hpelem[1] in candidate.possibleValueList):
                    retVal[index].possibleValueList.remove(hpelem[1])
    return retVal
            

# hidden pair example:
# set in which elements 3, 5 are only included in candidates c1, c2
# -> all elements beside 3, 5 can be removed from candidates c1, c2

# hidden pair: 3,5
candidateList1       = [candidate(0,0,[3 , 5, 6, 9]), candidate(0,0,[1, 2, 3, 5, 7, 8]), candidate(0,0,[6, 8, 9]), candidate(0,0,[6, 8, 9]), candidate(0,0,[6, 8])] 
expectedReducedList1 = [       [6, 9], [1, 2, 7, 8]      , [6, 8, 9], [6, 8, 9], [6, 8]]

# same as before, but 3 is also included as singles in other elements -> no hidden pair
candidateList2       = [candidate(0,0,[3 , 5, 6, 9]), candidate(0,0,[1, 2, 3, 5, 7, 8]), candidate(0,0,[3, 6, 8, 9]), candidate(0,0,[6, 8, 9]), candidate(0,0,[6, 8])] 
expectedReducedList2 = [[3 , 5, 6, 9], [1, 2, 3, 5, 7, 8], [3, 6, 8, 9], [6, 8, 9], [6, 8]] 

# no hidden pair
candidateList3       = [candidate(0,0,[1, 2, 3, 4, 5]), candidate(0,0,[1, 2, 3]), candidate(0,0,[3, 6, 7]), candidate(0,0,[1, 7, 8])]
expectedReducedList3 = [[1, 2, 3, 4, 5], [1, 2, 3], [3, 6, 7], [1, 7, 8]]

# two hidden pairs
candidateList4       = [candidate(0,0,[1, 2, 3, 4]), candidate(0,0,[3, 4, 5, 6, 8]), candidate(0,0,[5, 6, 7, 9])]
expectedReducedList4 = [      [1, 2],             [8],       [7, 9]]

# hidden pair: 2,3
candidateList5       = [candidate(0,0,[1, 2, 3, 5]), candidate(0,0,[2, 3, 4]), candidate(0,0,[4, 9]), candidate(0,0,[7, 8, 9])]
expectedReducedList5 = [      [1, 5],       [4], [4, 9], [7, 8, 9]]

allCandidateListOfLists = [candidateList1,candidateList2,candidateList3,candidateList4,candidateList5]
expected = [expectedReducedList1,expectedReducedList2,expectedReducedList3,expectedReducedList4,expectedReducedList5]
for index, candidateList in enumerate(allCandidateListOfLists):
    expectedReducedList = expected[index]
    possibleValueList = []
    for candidate in candidateList:
        possibleValueList.append(candidate.possibleValueList)
    print( f"\n==============   Input: {possibleValueList}")
    reducedCandidateList=getReducedCandidateList(possibleValueList,1)
    xy=getReducedCandidateList2(candidateList,1)
    print(xy)
    print(   f"Reduced candidate list: {reducedCandidateList}")
    if reducedCandidateList==expectedReducedList:
        print("... getReducedCandidateList test is PASS")
    else:
        print("... getReducedCandidateList test is FAIL")




