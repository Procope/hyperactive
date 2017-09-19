Solving a sudoku with Pycosat, zChaff, and Walksat
==================================================
source: [Kaggle sudoku dataset](https://www.kaggle.com/bryanpark/sudoku?) (1 million sudokus with solutions)

Minimal encoding [(Lynce, Inês, and Joël Ouaknine. "Sudoku as a SAT Problem.")](http://sat.inesc.pt/~ines/publications/aimath06.pdf)
----------------


#### Quiz #1
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

#### Solution #1
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
Max Decision Level                        0
Num. of Decisions                         1
( Stack + Vsids + Shrinking Decisions )   0 + 0 + 0
Original Num Variables                    729
Original Num Clauses                      8864
Original Num Literals                     18260
Added Conflict Clauses                    0
Num of Shrinkings                         0
Deleted Conflict Clauses                  0
Deleted Clauses                           0
Added Conflict Literals                   0
Deleted (Total) Literals                  0
Number of Implication                     729
Total Run Time                            0.000147
RESULT: SAT
```

### Walksat [best, noise 50 / 100]
Assignment found.

```
numatom = 729, numclause = 8864, numliterals = 18260
total elapsed seconds = 0.020000
average flips per second = 1212500
number solutions found = 10
final success rate = 100.000000
average length successful tries = 2425
average flips per assign (over all runs) = 2425.000000
average seconds per assign (over all runs) = 0.002000
mean flips until assign = 2425.000000
  variance = 1629958.000000
  standard deviation = 1276.698085
  standard error of mean = 403.727383
mean seconds until assign = 0.002000
  variance = 0.000001
  standard deviation = 0.001053
  standard error of mean = 0.000333
mean restarts until assign = 1.000000
  variance = 0.000000
  standard deviation = 0.000000
  standard error of mean = 0.000000
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 5.352958
      overall mean meanbad std deviation = 2.766404
      overall ratio mean numbad to mean std dev = 1.934988
    statistics on successful runs:
      successful mean average numbad = 5.352958
      successful mean numbad std deviation = 2.766404
      successful ratio mean numbad to mean std dev = 1.934988
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 0.000000
      nonsuccessful mean numbad std deviation = 0.000000
      nonsuccessful ratio mean numbad to mean std dev = 0.000000
ASSIGNMENT FOUND
```

### Walksat [novelty, noise 50 / 100]
Assignment found.

```
total elapsed seconds = 0.020000
average flips per second = 1597400
number solutions found = 10
final success rate = 100.000000
average length successful tries = 3194
average flips per assign (over all runs) = 3194.800000
average seconds per assign (over all runs) = 0.002000
mean flips until assign = 3194.800000
  variance = 8606770.622222
  standard deviation = 2933.729814
  standard error of mean = 927.726825
mean seconds until assign = 0.002000
  variance = 0.000003
  standard deviation = 0.001837
  standard error of mean = 0.000581
mean restarts until assign = 1.000000
  variance = 0.000000
  standard deviation = 0.000000
  standard error of mean = 0.000000
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 4.925996
      overall mean meanbad std deviation = 1.984125
      overall ratio mean numbad to mean std dev = 2.482705
    statistics on successful runs:
      successful mean average numbad = 4.925996
      successful mean numbad std deviation = 1.984125
      successful ratio mean numbad to mean std dev = 2.482705
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 0.000000
      nonsuccessful mean numbad std deviation = 0.000000
      nonsuccessful ratio mean numbad to mean std dev = 0.000000
ASSIGNMENT FOUND
```

### Walksat [rnovelty, noise 50 / 100]
Assignment found.

```
total elapsed seconds = 0.080000
average flips per second = 1818725
number solutions found = 10
final success rate = 100.000000
average length successful tries = 14549
average flips per assign (over all runs) = 14549.800000
average seconds per assign (over all runs) = 0.008000
mean flips until assign = 14549.800000
  variance = 274765770.177778
  standard deviation = 16576.060152
  standard error of mean = 5241.810471
mean seconds until assign = 0.008000
  variance = 0.000083
  standard deviation = 0.009114
  standard error of mean = 0.002882
mean restarts until assign = 1.000000
  variance = 0.000000
  standard deviation = 0.000000
  standard error of mean = 0.000000
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 5.877596
      overall mean meanbad std deviation = 2.410823
      overall ratio mean numbad to mean std dev = 2.438004
    statistics on successful runs:
      successful mean average numbad = 5.877596
      successful mean numbad std deviation = 2.410823
      successful ratio mean numbad to mean std dev = 2.438004
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 0.000000
      nonsuccessful mean numbad std deviation = 0.000000
      nonsuccessful ratio mean numbad to mean std dev = 0.000000
ASSIGNMENT FOUND
```

### Walksat [random]
Assignment not found.

```
total elapsed seconds = 0.540000
average flips per second = 1851851
number solutions found = 0
final success rate = 0.000000
average length successful tries = 0
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 57.118897
      overall mean meanbad std deviation = 6.826878
      overall ratio mean numbad to mean std dev = 8.366767
    statistics on successful runs:
      successful mean average numbad = 0.000000
      successful mean numbad std deviation = 0.000000
      successful ratio mean numbad to mean std dev = 0.000000
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 57.118897
      nonsuccessful mean numbad std deviation = 6.826878
      nonsuccessful ratio mean numbad to mean std dev = 8.366767
ASSIGNMENT NOT FOUND
```
