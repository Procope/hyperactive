Solving a sudoku with Pycosat, zChaff, and Walksat
==================================================
source: [Kaggle sudoku dataset](https://www.kaggle.com/bryanpark/sudoku?) (1 million sudokus with solutions)

### Sudoku #1

#### Quiz
```
[0 0 4 3 0 0 2 0 9]
[0 0 5 0 0 9 0 0 1]
[0 7 0 0 6 0 0 4 3]
[0 0 6 0 0 2 0 8 7]
[1 9 0 0 0 7 4 0 0]
[0 5 0 0 8 3 0 0 0]
[6 0 0 0 0 0 1 0 5]
[0 0 3 5 0 8 6 9 0]
[0 4 2 9 1 0 3 0 0]
```

#### Solution
```
[8 6 4 3 7 1 2 5 9]
[3 2 5 8 4 9 7 6 1]
[9 7 1 2 6 5 8 4 3]
[4 3 6 1 9 2 5 8 7]
[1 9 8 6 5 7 4 3 2]
[2 5 7 4 8 3 9 1 6]
[6 8 9 7 3 4 1 2 5]
[7 1 3 5 2 8 6 9 4]
[5 4 2 9 1 6 3 7 8]
```

SAT solvers
-----------

### Pycosat
Assignment found.

```
[8 6 4 3 7 1 2 5 9]
[3 2 5 8 4 9 7 6 1]
[9 7 1 2 6 5 8 4 3]
[4 3 6 1 9 2 5 8 7]
[1 9 8 6 5 7 4 3 2]
[2 5 7 4 8 3 9 1 6]
[6 8 9 7 3 4 1 2 5]
[7 1 3 5 2 8 6 9 4]
[5 4 2 9 1 6 3 7 8]
```

### zChaff
Assignment found.

```
Max Decision Level                          0
Num. of Decisions                           1
( Stack + Vsids + Shrinking Decisions )     0 + 0 + 0
Original Num Variables                      729
Original Num Clauses                        12023
Original Num Literals                       26279
Added Conflict Clauses                      0
Num of Shrinkings                           0
Deleted Conflict Clauses                    0
Deleted Clauses                             0
Added Conflict Literals                     0
Deleted (Total) Literals                    0
Number of Implication                       729
Total Run Time                              0.000515
RESULT: SAT
```

### Walksat [best, noise 50 / 100]
Assignment found.

```
numatom = 729, numclause = 12023, numliterals = 26279
total elapsed seconds = 0.010000
average flips per second = 718100
number solutions found = 1
final success rate = 100.000000
average length successful tries = 7181
average flips per assign (over all runs) = 7181.000000
average seconds per assign (over all runs) = 0.010000
mean flips until assign = 7181.000000
mean seconds until assign = 0.010000
mean restarts until assign = 1.000000
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 20.940000
      overall mean meanbad std deviation = 6.828542
      overall ratio mean numbad to mean std dev = 3.066541
    statistics on successful runs:
      successful mean average numbad = 20.940000
      successful mean numbad std deviation = 6.828542
      successful ratio mean numbad to mean std dev = 3.066541
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 0.000000
      nonsuccessful mean numbad std deviation = 0.000000
      nonsuccessful ratio mean numbad to mean std dev = 0.000000
ASSIGNMENT FOUND
```

### Walksat [novelty, noise 50 / 100]
Assignment found

```
tail starts after flip = 2187
total elapsed seconds = 0.010000
average flips per second = 489800
number solutions found = 1
final success rate = 100.000000
average length successful tries = 4898
average flips per assign (over all runs) = 4898.000000
average seconds per assign (over all runs) = 0.010000
mean flips until assign = 4898.000000
mean seconds until assign = 0.010000
mean restarts until assign = 1.000000
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 36.074074
      overall mean meanbad std deviation = 14.528291
      overall ratio mean numbad to mean std dev = 2.483023
    statistics on successful runs:
      successful mean average numbad = 36.074074
      successful mean numbad std deviation = 14.528291
      successful ratio mean numbad to mean std dev = 2.483023
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 0.000000
      nonsuccessful mean numbad std deviation = 0.000000
      nonsuccessful ratio mean numbad to mean std dev = 0.000000
ASSIGNMENT FOUND
```

### Walksat [rnovelty, noise 50 / 100]
Assignment found

```
total elapsed seconds = 0.010000
average flips per second = 429700
number solutions found = 1
final success rate = 100.000000
average length successful tries = 4297
average flips per assign (over all runs) = 4297.000000
average seconds per assign (over all runs) = 0.010000
mean flips until assign = 4297.000000
mean seconds until assign = 0.010000
mean restarts until assign = 1.000000
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 21.619048
      overall mean meanbad std deviation = 6.888223
      overall ratio mean numbad to mean std dev = 3.138552
    statistics on successful runs:
      successful mean average numbad = 21.619048
      successful mean numbad std deviation = 6.888223
      successful ratio mean numbad to mean std dev = 3.138552
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 0.000000
      nonsuccessful mean numbad std deviation = 0.000000
      nonsuccessful ratio mean numbad to mean std dev = 0.000000
ASSIGNMENT FOUND
```

### Walksat [random]
Assignment not found

```
total elapsed seconds = 0.870000
average flips per second = 1149425
number solutions found = 0
final success rate = 0.000000
average length successful tries = 0
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 152.578243
      overall mean meanbad std deviation = 13.940760
      overall ratio mean numbad to mean std dev = 10.944758
    statistics on successful runs:
      successful mean average numbad = 0.000000
      successful mean numbad std deviation = 0.000000
      successful ratio mean numbad to mean std dev = 0.000000
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 152.578243
      nonsuccessful mean numbad std deviation = 13.940760
      nonsuccessful ratio mean numbad to mean std dev = 10.944758
ASSIGNMENT NOT FOUND
```
