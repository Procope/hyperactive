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

def atmost_cell(names):
    encode = []
    n = names.shape[0]
    for i in range(n):
        for j in range(n):
            for k in range(n-1):
                for l in range(k+1, n):
                    arr = [int(-names[i,j,k]), int(-names[i,j,l])]
                    encode.append(arr)
    return encode

def atleast_cell(names):
    encode = []
    n = names.shape[0]
    for i in range(n):
        for j in range(n):
            arr = [int(names[i][j][k]) for k in range(n)]
            encode.append(arr)
    return encode

def exactly_one(names):
    enc1 = atmost_cell(names)
    enc2 = atleast_cell(names)
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

def atleast_block(names):
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

def atmost_block(names):
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

def exactly_one_block(names):
    enc1 = atmost_block(names)
    enc2 = atleast_block(names)
    return enc1 + enc2


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 16:20:30 2017

@author: jackharding
"""
import pycosat
import numpy as np
from math import sqrt



#READ ME: I think I've used a slightly different indexing convention (sorry!)
#Under my convention, variables are lists of length 3. They are of the form
#[row, column, value] (so [1, 1, 1] means the variable which has value 1 in row 1 and column 1)
#In my mind, this is the most intuitive labelling system, but it shouldn't take any effort to move
#between the two (though we will need to change either the index on this file or the original one).


#function which, given a sudoku, creates a list of the assigned variables
#(note that indexing might be a little different)
def assigned_variables(sample_sudoku):
    assigned = []
    for i in range(9):
        for j in range(9):
            value = sample_sudoku[i][j]
            if value > 0:
                assigned.append([i + 1, j + 1, value])
    return assigned

#function which, given two variables (in index form), decides if they are in the same cell
#with different values
def same_Cell(var_1, var_2):
    a, b, c = var_1[0], var_1[1], var_1[2]
    d, e, f = var_2[0], var_2[1], var_2[2]
    if a == d and b == e and c != f:
        return True
    return False

#function which, given two variables, decides if they are in the same row
#with the same value
def same_Row(var_1, var_2):
    a, b, c = var_1[0], var_1[1], var_1[2]
    d, e, f = var_2[0], var_2[1], var_2[2]
    if a == d and b != e and c == f:
        return True
    return False

#function which, given two variables, decides if they are in the same column
#with the same value
def same_Column(var_1, var_2):
    a, b, c = var_1[0], var_1[1], var_1[2]
    d, e, f = var_2[0], var_2[1], var_2[2]
    if a != d and b == e and c == f:
        return True
    return False

#function which, given any index (e.g. [5, 3, 1]), and the length of the sudoku under consideration, returns the index
#of the top left square in the box where it is located (in this case, [4,1])
def top_left_square(variable, length_of_sudoku):
    top_left = [1,1]
    row, column = variable.copy()[0], variable.copy()[1]
    while (row - sqrt(length_of_sudoku)) > 0:
        row -= sqrt(length_of_sudoku)
        top_left[0] += int(sqrt(length_of_sudoku))
    while (column - sqrt(length_of_sudoku)) > 0:
        column -= sqrt(length_of_sudoku)
        top_left[1] += int(sqrt(length_of_sudoku))
    return top_left

#function which, given two variables, decides if they are in the same block
#with the same value
def same_Block(var_1, var_2, length_of_sudoku):
    if var_1 == var_2:
        return False
    if var_1[2] == var_2[2]:
        if top_left_square(var_1, length_of_sudoku) == top_left_square(var_2, length_of_sudoku):
            return True
    return False

#function which returns length of one side of the sudoku
def length(sample_sudoku):
    return len(sample_sudoku[0])

#function which, given a sudoku, outputs all the possible variables needed in that sudoku
def all_variables(sample_sudoku):
    variable_list = []
    for rows in range(1, length(sample_sudoku) + 1):
            for columns in range(1, length(sample_sudoku) + 1):
                    for values in range(1, length(sample_sudoku) + 1):
                        variable_list.append([rows, columns, values])
    return variable_list

#function which, given all the variables, creates a list of the variables which the assignment renders immediately false
#e.g. if [1, 1, 1] is in "assigned", this list will include [2, 1, 1], [3, 1, 1], etc
def create_falsehoods(sample_sudoku):
    variables = all_variables(sample_sudoku)
    falsehoods = []
    for truths in assigned_variables(sample_sudoku):
        for members in variables:
            if same_Cell(truths, members):
                falsehoods.append(members)
            if same_Row(truths, members):
                falsehoods.append(members)
            if same_Column(truths, members):
                falsehoods.append(members)
            if same_Block(truths, members, length(sample_sudoku)):
                falsehoods.append(members)
    return falsehoods


#turns a variable "[row, column, value]" into a number
#(NOTE: using my indexing) Need to check indexing is working correctly.
def encode_into_number(variable, sample_sudoku):
    row, column, value = variable[0], variable[1], variable[2]
    n = length(sample_sudoku)
    return (row - 1) * (n**2) + (column - 1) * n + (value - 1) + 1

#function which, given an encoding and a sudoku,
#outputs a trimmed down list of clauses
#The 'reduction operators' from the paper are basically contained
#within the if clauses in the function body

def trim_down_encoding(encoding, sample_sudoku):
    assigned = [encode_into_number(x, sample_sudoku) for x in assigned_variables(sample_sudoku)]
    false = [encode_into_number(x, sample_sudoku) for x in create_falsehoods(sample_sudoku)]
    new_encoding = encoding.copy()
    for clause in new_encoding.copy():
        for literal in clause.copy():
            if literal in assigned:
                new_encoding.remove(clause)
                break
            if -literal in false:
                new_encoding.remove(clause)
                break
            if literal in false:
                clause.remove(literal)
            if -literal in assigned:
                clause.remove(literal)
    return new_encoding


def to_cnf_file(encoding, filename):
        with open(filename, 'w') as f:
            print("p cnf {} {}".format(9**3, len(encoding)), file=f)
            for clause in encoding:
                for literal in clause:
                    print(literal, " ", end='', file=f)
                print("0", file=f)

def to_cnf_string(encoding):
    string = "p cnf {} {}\n".format(9**3, len(encoding))
    for clause in encoding:
        string += ' ' .join([str(literal) for literal in clause])
        string += ' 0\n'
    return string


def extended_encoding(names):
    encoding = []
    encoding.extend(exactly_one(names))
    encoding.extend(exactly_one_row(names))
    encoding.extend(exactly_one_column(names))
    encoding.extend(exactly_one_block(names))

    return encoding


def minimal_encoding(names):
    encoding = []
    encoding.extend(atleast_cell(names))
    encoding.extend(atmost_row(names))
    encoding.extend(atmost_column(names))
    encoding.extend(atmost_block(names))

    return encoding


def efficient_encoding(names):
    encoding = []
    encoding.extend(atleast_cell(names))
    encoding.extend(atmost_cell(names))
    encoding.extend(atmost_row(names))
    encoding.extend(atmost_column(names))
    encoding.extend(atmost_block(names))

    return encoding

def optimised_encoding(names, sample_sudoku):
    encoding = extended_encoding(names)
    return trim_down_encoding(encoding, sample_sudoku)

if __name__ == "__main__":
    names, ids = create_sudoku_vars(n = 9)

    min_encoding = minimal_encoding(names)
    ext_encoding = extended_encoding(names)
    eff_encoding = efficient_encoding(names)

    # # print(encoding)

    s_test = [[0, 0, 4, 3, 0, 0, 2, 0, 9],
                [0, 0, 5, 0, 0, 9, 0, 0, 1],
                [0, 7, 0, 0, 6, 0, 0, 4, 3],
                [0, 0, 6, 0, 0, 2, 0, 8, 7],
                [1, 9, 0, 0, 0, 7, 4, 0, 0],
                [0, 5, 0, 0, 8, 3, 0, 0, 0],
                [6, 0, 0, 0, 0, 0, 1, 0, 5],
                [0, 0, 3, 5, 0, 8, 6, 9, 0],
                [0, 4, 2, 9, 1, 0, 3, 0, 0]]

def givens(sample_sudoku):
    return encode_into_number(assigned(sample_sudoku))

print(givens(s_test))

    print(to_cnf_string(min_encoding))
    # to_cnf(min_encoding, "min_encod.cnf")
    # to_cnf(ext_encoding, "ext_encod.cnf")
    # to_cnf(eff_encoding, "eff_encod.cnf")

    # solution = pycosat.solve(encoding)
    # sol = np.zeros((9,9), dtype=np.int)
    # for s in solution:
    #     if s > 0:
    #         (i,j,k) = ids[s]
    #         sol[i-1][j-1] = k
    # print(sol)

    # i = 0
    # for s in pycosat.itersolve(encoding):
    #     i += 1
    #     if i % 1000 == 0:
    #         print(i)
# print(optimised_encoding(encoding, s_test))


    # solution = [8, 15, 22, 30, 43, 46, 56, 68, 81, 84, 92,
    #  104, 116, 121, 135, 142, 150, 154, 171, 178, 181,
    #   191, 204, 212, 224, 229, 237, 247, 255, 267,271,
    #   288, 290, 302, 314, 322, 325, 342, 350, 357, 365,
    #   376, 382, 390, 398, 407, 419, 430, 436, 449, 453,
    #   468, 469, 483, 492, 503, 513, 520, 525, 535, 541,
    #   551, 563, 574, 577, 588, 599, 605, 620, 627, 639,
    #   643, 653, 661, 668, 684, 685, 699, 705, 718, 728]

    #   8, 15, 22, 30, 43, 46, 56, 68, 81, 84, 92, 104, 116, 121, 135, 142, 150, 154, 171, 178, 181, 191, 204, 212, 224, 229, 237, 247, 255, 267, 271, 288, 290, 302, 314, 322, 325, 342, 350, 357, 365, 376, 382, 390, 398, 407, 419, 430, 436, 449, 453, 468, 469, 483, 492, 503, 513, 520, 525, 535, 541, 551, 563, 574, 577, 588, 599, 605, 620, 627, 639, 643, 653, 661, 668, 684, 685, 699, 705, 718, 728

    # sol = np.zeros((9,9), dtype=np.int)
    # for s in solution:
    #     if s > 0:
    #         (i,j,k) = ids[s]
    #         sol[i-1][j-1] = k

    # print(sol)
