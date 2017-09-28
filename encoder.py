import pycosat
import numpy as np
from math import sqrt


def create_sudoku_vars(n=9):
    names = np.zeros([n,n,n], dtype = np.int)
    ids = list()
    ids.append((-1,-1,-1))
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


def to_cnf_file(encoding, filename):
        with open(filename, 'w') as f:
            print("p cnf {} {}".format(9**3, len(encoding)), file=f)
            for clause in encoding:
                # for literal in clause:
                print(' ' .join([str(literal) for literal in clause]), end='', file=f)
                print(" 0", file=f)
                    # print(literal, " ", end='', file=f)
                # print("0", file=f)

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
    for truth in assigned_variables(sample_sudoku):
        for member in variables:
            if same_Cell(truth, member):
                falsehoods.append(member)
            if same_Row(truth, member):
                falsehoods.append(member)
            if same_Column(truth, member):
                falsehoods.append(member)
            if same_Block(truth, member, length(sample_sudoku)):
                falsehoods.append(member)
    return falsehoods

#turns a variable "[row, column, value]" into a number
#(NOTE: using my indexing) Need to check indexing is working correctly.
def encode_into_number(variable, sample_sudoku):
    row, column, value = variable[0], variable[1], variable[2]
    n = length(sample_sudoku)
    return int((row - 1) * (n**2) + (column - 1) * n + value)

#function which, given an encoding and a sudoku,
#outputs a trimmed down list of clauses
#The 'reduction operators' from the paper are basically contained
#within the if clauses in the function body

def optimised_encoding(encoding, sample_sudoku):
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
    for literal in assigned:
        new_encoding.append([literal])
    for literal in false:
        new_encoding.append([-literal])
    return new_encoding

#new_encoding = optimised_encoding(encoding, s_test)
#print("Number of clauses in old encoding:", len(encoding))
#print("Number of clauses in new encoding:", len(new_encoding))
#def variable_counter(encoding):
#    counter = set()
#    for clause in encoding:
#        for literal in clause:
#            counter.add(literal**2)
#    return len(counter)
##
#print("Number of variables in old encoding:", variable_counter(encoding))
#print("Number of variables in new encoding:", variable_counter(new_encoding))

#function which calculates the top left of the hypersquare a given index is in
def top_left_hypersquare(variable, length_of_sudoku):
    top_left = [2,2]
    row, column = variable.copy()[0], variable.copy()[1]
    while row > sqrt(length_of_sudoku) + 1:
        row -= sqrt(length_of_sudoku) + 1
        top_left[0] += int(sqrt(length_of_sudoku) + 1)
    while column > sqrt(length_of_sudoku) + 1:
        column -= sqrt(length_of_sudoku) + 1
        top_left[1] += int(sqrt(length_of_sudoku) + 1)
    if row == 1:
        return None
    if column == 1:
        return None
    return top_left

#function which, given two variables, decides if they are in the same hypersquare with
#the same value
def incompatible_hyperBlock(var_1, var_2, length_of_sudoku):
    if var_1 == var_2:
        return False
    if top_left_hypersquare(var_1, length_of_sudoku) == None:
        return False
    if top_left_hypersquare(var_2, length_of_sudoku) == None:
        return False
    if var_1[2] == var_2[2]:
        if top_left_hypersquare(var_1, length_of_sudoku) == top_left_hypersquare(var_2, length_of_sudoku):
            return True
    return False

#function which outputs a list of hypersquare top left coordinates
def generate_top_left_of_hypersquares(length_of_sudoku):
    top_lefts_list = []
    for row in range(2, length_of_sudoku + 1, int(sqrt(length_of_sudoku) + 1)):
        for column in range(2, length_of_sudoku + 1, int(sqrt(length_of_sudoku) + 1)):
            top_lefts_list.append([row, column])
    return top_lefts_list

#function which says every number must appear at least once in each hypersquare
def at_least_hypersquare(sample_sudoku):
    length_of_sudoku = len(sample_sudoku)
    encoding = []
    for top_lefts in generate_top_left_of_hypersquares(length_of_sudoku):
        for row in range(int(sqrt(length_of_sudoku))):
            for column in range(int(sqrt(length_of_sudoku))):
                encoding.append([])
                for value in range(1, length_of_sudoku + 1):
                    encoding[-1].append(encode_into_number([top_lefts[0] + row, top_lefts[1] + column, value], sample_sudoku))
    return encoding

#print(at_least_hypersquare(81))

#function which says every number can appear at most once in each hypersquare(NEEDS OPTMISING)
def at_most_hypersquare(sample_sudoku):
    length_of_sudoku = len(sample_sudoku)
    encoding = []
    for var1 in all_variables(sample_sudoku):
        for var2 in all_variables(sample_sudoku):
                            if incompatible_hyperBlock(var1, var2, length_of_sudoku):
                                encoding.append([-encode_into_number(var1, sample_sudoku), -encode_into_number(var2, sample_sudoku)])
    return encoding

def exactly_one_hypersquare(sample_sudoku):
    return at_least_hypersquare(sample_sudoku) + at_most_hypersquare(sample_sudoku)

#
#
#implementing an optimised encoding for a hypersudoku
#
#


#function which, given all the variables, creates a list of the hyper_variables which the assignment renders immediately false
#e.g. if [1, 1, 1] is in "assigned", this list will include [2, 1, 1], [3, 1, 1], etc
def create_hyper_falsehoods(sample_sudoku):
    variables = all_variables(sample_sudoku)
    falsehoods = []
    for truth in assigned_variables(sample_sudoku):
        for member in variables:
            if same_Cell(truth, member):
                falsehoods.append(member)
            if same_Row(truth, member):
                falsehoods.append(member)
            if same_Column(truth, member):
                falsehoods.append(member)
            if same_Block(truth, member, length(sample_sudoku)):
                falsehoods.append(member)
            if incompatible_hyperBlock(truth, member, length(sample_sudoku)):
                falsehoods.append(member)
    return falsehoods


