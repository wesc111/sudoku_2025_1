
# a structure for candidates contain the row, col and the list of possible values
class candidate:
    def __init__(self, row, col, candidateList):
        self.row = row
        self.col = col
        self.candidateList = candidateList

    def __str__(self):
        return f"Candidates at row={self.row}, col={self.col}: {self.candidateList}"

def removeNakedTwinsInCandidateList_old_v1(cl):
    """function to find same doubles in a candidate list cl"""
    doubleList = []   # list to store all lists with 2 elements
    listofElementsinSameDoubles_1 = []
    clReturn = []
    candidateList = []
    for elem in cl:
        candidateList = elem.candidateList
        if len(candidateList) == 2:
            doubleList.append(candidateList)
    for elem in doubleList:
        doubleListWithoutActualElem = doubleList.copy()
        doubleListWithoutActualElem.remove(elem)
        if elem in doubleListWithoutActualElem:
            listofElementsinSameDoubles_1 += elem
    listofElementsinSameDoubles = sorted(list(set(listofElementsinSameDoubles_1)))
    # and now remove all elements from the candidate list that are in listofElementsinSameDoubles  
    for list1 in cl:    # for each list in the list of lists:      
        if len(list1) <= 2:   # don't change items that are 1 or 2 elements long
            candidateList.append(list1)
            continue   
        myList = list1.copy()
        for elem in list1:   # for each element in the list:
            if elem in listofElementsinSameDoubles:   # remove the element if it is in listofElementsinSameDoubles
                myList.remove(elem)
        candidateList.append(myList)
    clReturn.candidateList = candidateList
    return clReturn

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

# candidate lists
cl1 = [candidate(1, 2, [2, 7, 8]), candidate(1, 3, [2, 8]), candidate(1, 4, [2, 8]),  candidate(1, 5, [7, 9])]
cl2 = [candidate(3, 2,[1,2]), candidate(3, 2,[2, 3, 4, 7, 8]), candidate(3, 2,[2, 8]), candidate(3, 2,[2, 8]), candidate(3, 2,[7, 8, 9])]
cl3 = [candidate(4, 3, [2, 3, 5, 7, 8]), candidate(4, 5, [2, 8]), candidate(4, 6, [2, 8]),  candidate(4, 7, [3, 5]), candidate(4, 8, [3, 5]), candidate(4, 2, [2, 7, 9])]
cl4 = [candidate(8, 0, [1,2]), candidate(8, 1, [1,2]), candidate(8, 3, [5,6]), candidate(8, 4, [5,6]), candidate(8, 5, [1,2,3,4,5,6,7,8,9])]
cl5 = [candidate(3, 0, [1,2]), candidate(3, 1, [1,4]), candidate(3,3, [1,2,4,8,9])]
cl6 = [candidate(3, 0, [1,2]), candidate(3, 1, [2,1]), candidate(3,3, [1,2,4,8,9])]
print("\n===== Test of function removeNakedTwinsInCandidateList(cl) =====")

print("\n===== Test with cl1 =====")
print(f"cl1:")
for elem in cl1:
    print(elem)
cl1r = removeNakedTwinsInCandidateList(cl1)
print(f"Return value cl1r:")
for elem in cl1r:
    print(elem)

print("\n===== Test with cl2 =====")
print(f"cl2:")
for elem in cl2:
    print(elem)
cl2r = removeNakedTwinsInCandidateList(cl2)
print(f"Return value cl2r:")
for elem in cl2r:
    print(elem)


print("\n===== Test with cl3 =====")
print(f"cl3:")
for elem in cl3:
    print(elem)
cl3r = removeNakedTwinsInCandidateList(cl3)
print(f"Return value cl3r:")
for elem in cl3r:
    print(elem)

print("\n===== Test with cl4 =====")
print(f"cl4:")
for elem in cl4:
    print(elem)
cl4r = removeNakedTwinsInCandidateList(cl4)
print(f"Return value cl4r:")
for elem in cl4r:
    print(elem)

print("\n===== Test with cl5 =====")
print(f"cl5:")
for elem in cl5:
    print(elem)
cl5r = removeNakedTwinsInCandidateList(cl5)
print(f"Return value cl5r:")
for elem in cl5r:
    print(elem)

print("\n===== Test with cl6 =====")
print(f"cl6:")
for elem in cl6:
    print(elem)
cl6r = removeNakedTwinsInCandidateList(cl6)
print(f"Return value cl6r:")
for elem in cl6r:
    print(elem)