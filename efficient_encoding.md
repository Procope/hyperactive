Solving a sudoku with Pycosat, zChaff, and Walksat
==================================================
source: [Kaggle sudoku dataset](https://www.kaggle.com/bryanpark/sudoku?) (1 million sudokus with solutions)

Efficient encoding [(Weber, Tjark. "A SAT-based Sudoku Solver.")](https://www.researchgate.net/profile/Tjark_Weber/publication/228731990_A_SAT-based_Sudoku_solver/links/53e8b8bf0cf25d674ea8545a.pdf)
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
Original Num Clauses                      11780
Original Num Literals                     24092
Added Conflict Clauses                    0
Num of Shrinkings                         0
Deleted Conflict Clauses                  0
Deleted Clauses                           0
Added Conflict Literals                   0
Deleted (Total) Literals                  0
Number of Implication                     729
Total Run Time                            0.00056
RESULT: SAT

```

### Walksat [best, noise 50 / 100]
Assignment found.

```
numatom = 729, numclause = 11780, numliterals = 24092
total elapsed seconds = 0.030000
average flips per second = 609566
number solutions found = 10
final success rate = 100.000000
average length successful tries = 1828
average flips per assign (over all runs) = 1828.700000
average seconds per assign (over all runs) = 0.003000
mean flips until assign = 1828.700000
  variance = 628038.677778
  standard deviation = 792.488913
  standard error of mean = 250.606999
mean seconds until assign = 0.003000
  variance = 0.000002
  standard deviation = 0.001300
  standard error of mean = 0.000411
mean restarts until assign = 1.000000
  variance = 0.000000
  standard deviation = 0.000000
  standard error of mean = 0.000000
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 3.266667
      overall mean meanbad std deviation = 1.122973
      overall ratio mean numbad to mean std dev = 2.908945
    statistics on successful runs:
      successful mean average numbad = 3.266667
      successful mean numbad std deviation = 1.122973
      successful ratio mean numbad to mean std dev = 2.908945
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 0.000000
      nonsuccessful mean numbad std deviation = 0.000000
      nonsuccessful ratio mean numbad to mean std dev = 0.000000
ASSIGNMENT FOUND
```

### Walksat [novelty, noise 50 / 100]
Assignment found.

```
total elapsed seconds = 0.060000
average flips per second = 1364250
number solutions found = 10
final success rate = 100.000000
average length successful tries = 8185
average flips per assign (over all runs) = 8185.500000
average seconds per assign (over all runs) = 0.006000
mean flips until assign = 8185.500000
  variance = 73995185.388889
  standard deviation = 8602.045419
  standard error of mean = 2720.205606
mean seconds until assign = 0.006000
  variance = 0.000040
  standard deviation = 0.006305
  standard error of mean = 0.001994
mean restarts until assign = 1.000000
  variance = 0.000000
  standard deviation = 0.000000
  standard error of mean = 0.000000
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 4.752781
      overall mean meanbad std deviation = 2.291208
      overall ratio mean numbad to mean std dev = 2.074356
    statistics on successful runs:
      successful mean average numbad = 4.752781
      successful mean numbad std deviation = 2.291208
      successful ratio mean numbad to mean std dev = 2.074356
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 0.000000
      nonsuccessful mean numbad std deviation = 0.000000
      nonsuccessful ratio mean numbad to mean std dev = 0.000000
ASSIGNMENT FOUND
```

### Walksat [rnovelty, noise 50 / 100]
Assignment found.

```
total elapsed seconds = 0.110000
average flips per second = 1607236
number solutions found = 9
final success rate = 90.000000
average length successful tries = 8532
average flips per assign (over all runs) = 19644.000000
average seconds per assign (over all runs) = 0.012222
mean flips until assign = 19644.000000
  variance = 1050232567.000000
  standard deviation = 32407.291880
  standard error of mean = 10802.430627
mean seconds until assign = 0.012222
  variance = 0.000407
  standard deviation = 0.020163
  standard error of mean = 0.006721
mean restarts until assign = 1.111111
  variance = 0.111111
  standard deviation = 0.333333
  standard error of mean = 0.111111
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 6.292980
      overall mean meanbad std deviation = 2.427930
      overall ratio mean numbad to mean std dev = 2.591912
    statistics on successful runs:
      successful mean average numbad = 6.751576
      successful mean numbad std deviation = 2.913516
      successful ratio mean numbad to mean std dev = 2.317330
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 4.000000
      nonsuccessful mean numbad std deviation = 0.000000
      nonsuccessful ratio mean numbad to mean std dev = inf
ASSIGNMENT FOUND
```

### Walksat [random]
Assignment not found.

```
total elapsed seconds = 0.730000
average flips per second = 1369863
number solutions found = 0
final success rate = 0.000000
average length successful tries = 0
final numbad level statistics
    statistics over all runs:
      overall mean average numbad = 58.041164
      overall mean meanbad std deviation = 7.296874
      overall ratio mean numbad to mean std dev = 7.954251
    statistics on successful runs:
      successful mean average numbad = 0.000000
      successful mean numbad std deviation = 0.000000
      successful ratio mean numbad to mean std dev = 0.000000
    statistics on nonsuccessful runs:
      nonsuccessful mean average numbad level = 58.041164
      nonsuccessful mean numbad std deviation = 7.296874
      nonsuccessful ratio mean numbad to mean std dev = 7.954251
ASSIGNMENT NOT FOUND
```
