# test_candidate_p.py
# test bench for package candidate_p.py
# WSC, 2-Mar-2025

from candidate_p import candidate
from candidate_p import candidateList

import copy

# define tests that should run
#       0      1      2      3      4      5      6       7      8      9       10   11     12     13     14     15
test = [False, False, False, False, False, False, False , False, False, False, False, True, False, False, False, False]
testAll = False
testNum = 0

# some test data
cl1 = candidateList([candidate(0,1,[3 , 5, 6, 9]), candidate(0,2,[1, 2, 3, 5, 7, 8]), candidate(1,4,[6, 8, 9]), candidate(1,5,[6, 8, 9]), candidate(0,6,[6, 8])],"cl1")
cl4 = candidateList([candidate(2,0,[3,5]), candidate(2,4,[3,5]), candidate(2,5,[3,5]), candidate(2,6,[3,5,7])],"cl4")
cl5 = candidateList([candidate(2,0,[3,5]), candidate(2,4,[3,5]), candidate(2,5,[3,5]), candidate(2,6,[3,5,7])],"cl5")
cl6 = candidateList([candidate(2,0,[3,5]), candidate(2,4,[3,5]), candidate(2,5,[3,5]), candidate(2,6,[3,5,7,8])],"cl6")
cl7 = candidateList([candidate(2,0,[3,5]), candidate(2,4,[3,5,7,8,9]), candidate(2,5,[3,5]), candidate(2,6,[1,3,5,7])],"cl7")
c1 = candidate(2,0,[3,5])
c2 = candidate(2,1,[1,2,3,5])
c3 = candidate(2,2,[1])
c4 = candidate(2,0,[])
cl8 = candidateList([c1,c2,c3,c4])
cl9 = candidateList([candidate(2,0,[3,5]), candidate(2,4,[3,5,7,8,9]), candidate(2,5,[3,5]), candidate(2,6,[1,3,5,7]), candidate(2,7,[8])],"cl9")
cl10 = candidateList([candidate(3,0,[1]), candidate(3,4,[1,2,4,5]), candidate(3,5,[2]), candidate(3,6,[4]), candidate(3,7,[8,9]),candidate(3,8,[1,9])], "cl10")

# cl12: Singles: 8, 7, 3    Hidden singles: 5, 4
cl12 = candidateList([candidate(4,0,[8]), candidate(4,1,[7]), candidate(4,4,[1,2,3,5]), candidate(4,5,[1,2,3,4]), candidate(4,6,[3]), candidate(4,6,[7,8]) ], "cl12")
cl13 = candidateList([candidate(4,0,[1,2,7,8]), candidate(4,1,[1,2,3,4,5]), candidate(4,4,[3,4,8]) ], "cl13")

cl14 = candidateList([candidate(0, 0, [4, 5]), candidate(0, 1, [4, 5, 7, 8]), candidate(0, 3, [4, 9]), candidate(0, 5, [1, 4, 7]), candidate(0, 7, [5, 7, 8, 9]), candidate(0, 8, [5, 7])], "cl14")
cl15 = candidateList([candidate(0, 0, [1,2,3,4,5,6,7,8,9]), candidate(0, 1, [1,3,5,7,9]), candidate(0, 3, [2,4,6,8])], "cl15")

cl16 = candidateList([ candidate(3, 2, [2, 3, 8]), candidate(4, 0, [2, 6]), candidate(5, 0, [2, 4, 6]), candidate(5, 1, [4, 6]), candidate(5, 2, [2, 3, 8]) ],  "cl16")

cl17 = candidateList([ candidate(3, 2, [1, 3, 4, 5]), candidate(4, 0, [2, 5]), candidate(5, 0, [2, 5]), candidate(5, 1, [2,4,6]) ],  "cl17")
cl18 = candidateList([ candidate(0, 1, [3, 8]), candidate(3, 1, [1, 7]), candidate(4, 1, [1, 3, 7, 8]), candidate(6, 1, [2, 3, 7, 8]), candidate(7, 1, [2, 3, 7, 8]) ],  "cl18")

cl19 = candidateList([ candidate(3, 2, [1, 3, 4, 5]), candidate(4, 0, [1, 2, 5]), candidate(5, 0, [1, 2, 5]), candidate(6, 0, [1, 2, 5]), candidate(4,1, [6,7]), candidate(4,2, [6,7]), candidate(7, 0, [2, 4, 6]) ],  "cl19")

if testAll:
    for index, item in enumerate(test):
        test[index] = True

if (test[testNum]):  #0
    print(f"\n===== Test #{testNum}: defining cl1 and creating a copy cl2")
    cl2 = copy.deepcopy(cl1)
    cl2.setName("cl2")
    print(cl1)
    print(cl2)

    print(f"\n===== Test #{testNum}: appending some items to cl2")
    cl2.append(candidate(0,0,[2,4]))
    cl2.append(candidate(3,1,[1,2,3,4]))
    print(cl1)
    print(cl2)

    print(f"\n===== Test #{testNum}: removing item at 0,1 in cl2")
    cl2.remove_rc(0,1)
    print(cl2)

    print(f"\n===== Test #{testNum}: creating a copy of cl2 named cl3 and remove items equal to [6, 8, 9]")
    cl3 = copy.deepcopy(cl2)
    cl3.setName("cl3")
    cl3.remove_pv([6, 8, 9])
    print(cl2)
    print(cl3)
testNum += 1

if (test[testNum]):  #1
    print(f"\n===== Test #{testNum}: create cl4, remove all items equal to [3,5]")   
    print(cl4)
    cl4.remove_pv([3,5])
    print(cl4)
testNum += 1

if (test[testNum]):  #2
    print(f"\n===== Test #{testNum}: check the compare function")
    cl6 = copy.deepcopy(cl5)
    cl6.setName("cl6")
    print(cl5)
    print(cl6)
    cmpResult = cl5.compare(cl6)
    if cmpResult==True:
        print(f"PASS: compare result for equal lists is True")
    if cmpResult==False:
        print(f"FAIL: compare result for equal lists shall be True")
    print(cl5)
    print(cl6)
    cmpResult = cl5.compare(cl6)
    if cmpResult==False:
        print(f"PASS: compare result for equal lists is False")
    if cmpResult==True:
        print(f"PASS: compare result for equal lists is False")
testNum += 1

if (test[testNum]):  #3
    print(f"\n===== Test #{testNum}: check the len function")
    print(cl7)
    print(len(cl7))
    #for elem in candidateList:
    #    print(len(elem))
testNum += 1

if (test[testNum]):   #4
    print(f"\n===== Test #{testNum}: check candidate len function")
    cl8.setName("cl8")
    print(f"{c1}: len={len(c1)}")
    print(f"{c2}: len={len(c2)}")
    print(f"{c3}: len={len(c3)}")
    print(f"{c4}: len={len(c4)}")
    print(f"{cl8}: len={len(cl8)}")
testNum += 1

if (test[testNum]):   #5
    print(f"\n===== Test #{testNum}: check the iteration and len for each item of the candidateList")
    print(cl9)
    # iterate through the candidateList cl8
    for index, cc in enumerate(cl9):
        c1 = candidate(cc[0], cc[1], cc[2])
        print(f"{index}: {c1} -> len = {len(c1)}")
testNum += 1

if (test[testNum]):  #6
    print(f"\n===== Test #{testNum}: check candidateList.getSingles() and candidateList.getHiddenSingles()")   
    numSingles, cl10_s = cl10.getSingles()
    print(f"{cl10}")
    print(f"Singles found in cl10 -> num={numSingles}:")
    for elem in cl10_s:
        print("    Single",elem)
    numHiddenSingles, cl10_hs = cl10.getHiddenSingles()
    print(f"Hidden Singles found in cl12 -> num={numHiddenSingles}:")
    for elem in cl10_hs:
        print("    Hidden Single: ",elem)

    numSingles, cl12_s = cl12.getSingles()
    print(f"{cl12}")
    print(f"Singles found in cl12 -> num={numSingles}:")
    for elem in cl12_s:
        print("    Single",elem)
    numHiddenSingles, cl12_hs = cl12.getHiddenSingles()
    print(f"Hidden Singles found in cl12 -> num={numHiddenSingles}:")
    for elem in cl12_hs:
        print("    Hidden Single: ",elem)
testNum += 1

if (test[testNum]):  #7
    print(f"\n===== Test #{testNum}: check candidateList.reduceCandidateListForHiddenPairs()")
    print(cl13)
    cl13Reduced = cl13.reduceCandidateListForHiddenPairs(1)
    print(cl13Reduced)
    print("\n")
    print(cl14)
    cl14Reduced = cl14.reduceCandidateListForHiddenPairs(1)
    print(cl14Reduced)
    print("\n")
    print(cl16)
    cl16Reduced = cl16.reduceCandidateListForHiddenPairs(1)
    print(cl16Reduced)

     
testNum += 1

if (test[testNum]):  #8
    print(f"\n===== Test #{testNum}: check candidateList.removeElements")
    print(cl14)
    removeList=[1,2,3,4]
    cl14_r = cl14.removeElements(removeList)
    print(f"Candidate List with {removeList} removed: {cl14_r}")
    print(cl15)
    removeList=[1,3,5,7,9]
    cl15_r = cl14.removeElements(removeList)
    print(f"Candidate List with {removeList} removed: {cl15_r}")

    print(f"\n===== Test #{testNum}: check candidate.removeElements")
    t1 = candidate(1,1,[1,2,3,4,5,6,7,8,9])
    removeList=[2,4,6,8]
    print(f"Candidate {t1} with {removeList} removed: {t1.removeElements(removeList)}")
    removeList=[1,3,5,7,9]
    print(f"Candidate {t1} with {removeList} removed: {t1.removeElements(removeList)}")
    removeList=[9]
    print(f"Candidate {t1} with {removeList} removed: {t1.removeElements(removeList)}")
    removeList=[]
    print(f"Candidate {t1} with {removeList} removed: {t1.removeElements(removeList)}")
    removeList=[1,2,3,4,5,6,7,8,9]
    print(f"Candidate {t1} with {removeList} removed: {t1.removeElements(removeList)}")
testNum += 1

if (test[testNum]):  #9
    print(f"\n===== Test #{testNum}: check candidateList.count()")
    print(cl14)
    for i in range(1,10):
        print(f"{i}: count={cl14.count(i)}")
testNum += 1

if (test[testNum]):  #10
    print(f"\n===== Test #{testNum}: check candidateList.reduceCandidateListBesidePairs()")
    print(cl17)
    cl17Reduced = cl17.reduceCandidateListBesidePairs(1)
    print(cl17Reduced)
    print("\n",cl18)
    cl18Reduced = cl18.reduceCandidateListBesidePairs(1)
    print(cl18Reduced)
testNum += 1

if (test[testNum]):  #11
    print(f"\n===== Test #{testNum}: check candidateList.()")
    print(cl19)
    cl19_p = cl19.findPairs()
    cl19_t = cl19.findTripples()
    print("Found pairs: ", cl19_p)

    print("Found tripples: ", cl19_t)

    # TBD WSC
    cl19Reduced = cl19
    print(cl19Reduced)

testNum += 1

 