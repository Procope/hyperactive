# hyperactive

We encode Sudokus and Hyper Sudokus as SAT problems, solve them, and obtain some relevant (to us :)) statistics.

We use three types of encodings: _minimal encoding_, _extended encoding_, and _efficient encoding_.

The SAT solvers involved are PicoSAT (via [pycosat](https://github.com/ContinuumIO/pycosat) bindings), [zChaff](https://www.princeton.edu/~chaff/zchaff.html), and [WalkSAT](https://www.cs.rochester.edu/u/kautz/walksat).

### Run me
You need to install WalkSAT and zChaff first.

Packages required:

    pip install argparse
    pip install pycosat

Solve 10 standard Sudokus from a the provided data set (where _best_ indicates the WalkSAT variant to use; the other variants are _novelty_, and _rnovelty_)

    python solver.py data/sudoku_1000.csv 10 best

Solve 10 Hyper Sudokus from a the provided data set, using _novelty_ as a WalkSAT variant

    python hyper.py data/hyper.txt 30 novelty
