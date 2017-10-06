# hyperactive
Solving sudokus with SAT solvers.

We encode Sudokus and Hyper Sudokus as SAT problems, solve them, and obtain some relevant (to us :)) statistics.

We use three types of encodings: _minimal encoding_, _extended encoding_, and _efficient encoding_.

The SAT solvers involved are PicoSAT, zChaff, and WalkSAT.

### Run me
    python solver.py data/sudoku.csv 10 best
if you want to solve 10 standard sudokus from a data set. _best_ indicates the WalkSAT variant to use; the others are _novelty_, and _rnovelty_.

    python hyper.py data/hyper.txt 30 novelty
if you want to solve 30 Hyper Sudokus from a data set.
