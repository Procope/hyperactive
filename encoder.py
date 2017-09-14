import pycosat
import numpy as np
from math import sqrt


def create_sudoku_vars(n=9):
    names = np.zeros([n,n,n], dtype = np.int)
    ids = list()
    ids.append((-1,-1,-1))
    index = 1
    for i in range(n):
        for j in range(n):
            for k in range(n):
                name = i * n**2 + j * n + k+1
                names[i][j][k] = name
                ids.append((i+1,j+1,k+1))
    return names, ids


def get_name(names, i, j, k):
    return names[i-1, j-1, k-1]

def index_finder(enc, ids):
    for clause in enc:
        cl = ""
        for literal in clause:
            if literal < 0:
                cl = cl + "~" + str(ids[-literal]) + ", "
            else:
                cl = cl + str(ids[literal]) + ", "
        print(cl[:-2])

def encode_at_most_one(names):
    encode = []
    n = names.shape[0]
    for i in range(n):
        for j in range(n):
            for k in range(n-1):
                for l in range(k+1, n):
                    arr = [int(-names[i,j,k]), int(-names[i,j,l])]
                    encode.append(arr)
    return encode

def encode_at_least_one(names):
    encode = []
    n = names.shape[0]
    for i in range(n):
        for j in range(n):
            arr = [int(names[i][j][k]) for k in range(n)]
            encode.append(arr)
    return encode

def exactly_one(names):
    enc1 = encode_at_most_one(names)
    enc2 = encode_at_least_one(names)
    return enc1 + enc2

def atleast_column(names):
    encode = []
    n = names.shape[0]
    for j in range(n):
        for k in range(n):
            arr = [int(names[i][j][k]) for i in range(n)]
            encode.append(arr)
    return encode

def atmost_column(names):
    encode = []
    n = names.shape[0]
    for k in range(n):
        for l in range(n):
            for i in range(n-1):
                for j in range(i+1, n):
                    arr = [int(-names[i,k,l]), int(-names[j,k,l])]
                    encode.append(arr)
    return encode

def exactly_one_column(names):
    enc1 = atmost_column(names)
    enc2 = atleast_column(names)
    return enc1 + enc2

def atleast_row(names):
    encode = []
    n = names.shape[0]
    for i in range(n):
        for k in range(n):
            arr = [int(names[i][j][k]) for j in range(n)]
            encode.append(arr)
    return encode

def atmost_row(names):
    encode = []
    n = names.shape[0]
    for i in range(n):
        for l in range(n):
            for j in range(n-1):
                for k in range(j+1, n):
                    arr = [int(-names[i,j,l]), int(-names[i,k,l])]
                    encode.append(arr)
    return encode

def exactly_one_row(names):
    enc1 = atmost_row(names)
    enc2 = atleast_row(names)
    return enc1 + enc2

def atleast_region(names):
    encode = []
    n = names.shape[0]
    region_size = int(sqrt(n))

    for z in range(n):
        for i in range(region_size):
            for j in range(region_size):
                clause = []
                for x in range(region_size):
                    for y in range(region_size):
                        clause.append(int(names[3*i+x][3*j+y][z]))
                encode.append(clause)
    return encode

def atmost_region(names):
    encode = []
    n = names.shape[0]
    region_size = int(sqrt(n))

    for a in range(n):
        for b in range(region_size):
            for c in range(region_size):
                for d in range(region_size):
                    for e in range(region_size):
                        for f in range(e+1, region_size):
                            literal = int(-names[(region_size*b+d),(region_size*c+e), a])
                            literal2 = int(-names[(region_size*b+d),(region_size*c+f), a])
                            encode.append([literal, literal2])
                        for f in range(d+1, region_size):
                            for g in range(region_size):
                                literal = int(-names[(region_size*b+d),(region_size*c+e), a])
                                literal2 = int(-names[(region_size*b+f),(region_size*c+g), a])
                                encode.append([literal, literal2])
    return encode

def exactly_one_region(names):
    enc1 = atmost_region(names)
    enc2 = atleast_region(names)
    return enc1 + enc2


if __name__ == "__main__":
    names, ids = create_sudoku_vars(n = 9)
    encoding = []
    encoding.extend(exactly_one(names))
    encoding.extend(exactly_one_row(names))
    encoding.extend(exactly_one_column(names))
    encoding.extend(exactly_one_region(names))

    # print(encoding)

    s_test = [[8,0,6,5,0,0,0,0,0],
                [0,0,4,0,0,0,0,0,8],
                [0,0,0,0,0,0,6,0,0],
                [0,0,0,0,0,0,0,0,0],
                [3,7,0,4,5,0,0,0,0],
                [5,0,1,0,9,8,0,0,7],
                [0,0,0,0,0,7,0,2,0],
                [2,5,7,1,6,0,0,0,9],
                [0,8,0,0,3,0,0,4,0]]

    for i in range(9):
        for j in range(9):
            value = s_test[i][j]
            if value > 0:
                encoding.append([int(names[i, j, value - 1])])

    def to_cnf(encoding, filename):
        with open(filename, 'w') as f:
            print("p cnf {} {}".format(9**3, len(encoding)), file=f)
            for clause in encoding:
                for literal in clause:
                    print(literal, " ", end='', file=f)
                print("0", file=f)

    to_cnf(encoding, "test.cnf")

    # solution = pycosat.solve(encoding)
    # for s in solution:
    #     if s > 0:
    #         print(ids[s])
    # i = 0
    # for s in pycosat.itersolve(encoding):
    #     i += 1
    #     if i % 1000 == 0:
    #         print(i)



