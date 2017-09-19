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

s_test = [[8,0,6,0,0,0,0,0,0],
          [0,0,4,0,0,0,0,0,8],
          [0,0,0,0,0,0,6,0,0],
          [0,0,0,0,0,0,0,0,0],
          [3,7,0,4,5,0,0,0,0],
          [5,0,1,0,0,0,0,0,7],
          [0,0,0,0,0,0,0,2,0],
          [2,0,0,1,6,0,0,0,9],
          [0,8,0,0,0,0,0,4,0]]

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


#original encoder, for reference
#def create_sudoku_vars(n=9):
#    names = np.zeros([n,n,n], dtype = np.int)
#    ids = list()
#    ids.append((-1,-1,-1))
#    index = 1
#    for i in range(n):
#        for j in range(n):
#            for k in range(n):
#                name = i * n**2 + j * n + k+1
#                names[i][j][k] = name
#                ids.append((i+1,j+1,k+1))
#    return names, ids




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

def optimised_encoding(encoding, sample_sudoku):
    assigned = [encode_into_number(x) for x in assigned_variables(sample_sudoku)]
    false = [encode_into_number(x) for x in create_falsehoods(sample_sudoku)]
    new_encoding = encoding.copy()
    for clause in new_encoding:
        for literal in clause:
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

print(optimised_encoding(encoding, s_test))

            