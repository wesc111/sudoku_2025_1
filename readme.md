# Sudoku

A basic class library to solve sudokus with an example solver

Werner Schoegler, 17-Mar-2025

## Files included in this library

### Python files

| File | Description |
| ----------- | ----------- |
| candidate_p.py | package defining a class candidate and a class candidateList |
| sudoku.py | main program to solve sudokus (see usage description below) |
| sudoku_p.py | package defining a sudoku class that can be used used to solve sudokus |
| sudoku_io.py | file IO routines to read sudoku files |

### Test files

Files from project Solving Every Sudoku Puzzle on github, https://github.com/dimitri/sudoku/tree/master
 - easy_50.txt
 - hardest.txt
 - top95.txt

 My own files
 - sudoku_1.txt ... some collection from the past
 - sudoku_2.txt ... some SUDOKUs published in the NYT 2025

 ## Running the sudoku solver
 To run the sudoku solver, command line arguments can be used for control

 Command line argument -h shows the usage

```
> python sudoku.py -h
Optional arguments for sudoku_ex1:
    -h               ... print help
    -v               ... show program version
    -debug           ... show detailed debug info
    -num 2           ... solve SUDOKU #3
    -all             ... solve all SUDOKUs read from input file
    -noprint         ... no print of SUDOKU solution, just print PASS/FAIL results
    -f sudoku_1.txt  ... read SUDOKUs from file sudoku_1.txt
```

## Description of the solver algorithm
The solver algorithm is based on algorithms used by humans to solve such puzzles.

So main information used for solving are candidate lists. For each empty field of the SUDOKU a candidate list is created, and based on that candidate lists solving algorithms are used.

These algorithms are
- Singes
- Hidden Singles
- Pairs
- Hidden Pairs
- Tripples

If the solver is not successful based on above algorithms, the solver starts to use random guesses for Pairs. After doing a guess, the solver checks with above algorithms if a solution is found. If not, another guess is done and so on till either a solution is found or a max number for guesses is reached.
 