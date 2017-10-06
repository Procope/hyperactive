import pycosat
import numpy as np
from math import sqrt


def create_sudoku_vars(n=9):
    """
    Create propositional variables and name them.
    """
    names = np.zeros([n, n, n], dtype = np.int)
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
    """
    Friendly indexing.
    """
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


def to_cnf_file(encoding, filename):
    """
    Convert set of CNF clauses to DIMACS format and write it in a file.
    """
    with open(filename, 'w') as f:
        print("p cnf {} {}".format(9**3, len(encoding)), file=f)
        for clause in encoding:
            if len(clause) > 0:
                print(' ' .join([str(literal) for literal in clause]), end='', file=f)
                print(" 0", file=f)


def to_cnf_string(encoding):
    """
    Return the set of CNF clauses converted to DIMACS format.
    """
    string = "p cnf {} {}\n".format(9**3, len(encoding))
    for clause in encoding:
        if len(clause) > 0:
            string += ' ' .join([str(literal) for literal in clause])
            string += ' 0\n'
    return string


# Define all sets of clauses to compose into different encodings

# Each cell must contain at most one number
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


# At least one number appears in each cell.
def atleast_cell(names):
    encode = []
    n = names.shape[0]
    for i in range(n):
        for j in range(n):
            arr = [int(names[i][j][k]) for k in range(n)]
            encode.append(arr)
    return encode


# At most one number appears in each cell.
def exactly_one(names):
    enc1 = atmost_cell(names)
    enc2 = atleast_cell(names)
    return enc1 + enc2


# In each column, each number appears at least once.
def atleast_column(names):
    encode = []
    n = names.shape[0]
    for j in range(n):
        for k in range(n):
            arr = [int(names[i][j][k]) for i in range(n)]
            encode.append(arr)
    return encode


# In each column, each number appears at most once.
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


# In each column, each number appears exactly once.
def exactly_one_column(names):
    enc1 = atmost_column(names)
    enc2 = atleast_column(names)
    return enc1 + enc2


# In each row, each number appears at least once.
def atleast_row(names):
    encode = []
    n = names.shape[0]
    for i in range(n):
        for k in range(n):
            arr = [int(names[i][j][k]) for j in range(n)]
            encode.append(arr)
    return encode


# In each row, each number appears at most once.
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


# In each row, each number appears exactly once.
def exactly_one_row(names):
    enc1 = atmost_row(names)
    enc2 = atleast_row(names)
    return enc1 + enc2


# In each 3 × 3 block, each number appears at least once.
def atleast_block(names):
    encode = []
    n = names.shape[0]
    region_size = int(sqrt(n))

    for z in range(n):
        clause = []
        for i in range(region_size):
            for j in range(region_size):
                for x in range(region_size):
                    for y in range(region_size):
                        clause.append(int(names[3*i+x][3*j+y][z]))
                encode.append(clause)
    return encode


# In each 3 × 3 block, each number appears at most once.
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


# In each 3 × 3 block, each number appears exactly once.
def exactly_one_block(names):
    enc1 = atmost_block(names)
    enc2 = atleast_block(names)
    return enc1 + enc2


# Now the hyperconstraints. But first, some helper functions:

def top_left_hypersquare(variable, length_of_sudoku):
    """
    Return the top left cell of the hypersquare variable lies in
    """
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


def incompatible_hyperBlock(var_1, var_2, length_of_sudoku):
    """
    Return true if two variables belonging to the same hyperblock
    have the same value and the two variables are not equal.
    """
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


def generate_top_left_of_hypersquares(length_of_sudoku):
    """
    Return a list of list of hypersquare top left coordinates.
    """
    top_lefts_list = []
    for row in range(2, length_of_sudoku + 1, int(sqrt(length_of_sudoku) + 1)):
        for column in range(2, length_of_sudoku + 1, int(sqrt(length_of_sudoku) + 1)):
            top_lefts_list.append([row, column])
    return top_lefts_list


# Each number must appear at least once in each hypersquare.
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


# Each number can appear at most once in each hypersquare.
def at_most_hypersquare(sample_sudoku):
    length_of_sudoku = len(sample_sudoku)
    encoding = []
    for var1 in all_variables(sample_sudoku):
        for var2 in all_variables(sample_sudoku):
                            if incompatible_hyperBlock(var1, var2, length_of_sudoku):
                                encoding.append([-encode_into_number(var1, sample_sudoku), -encode_into_number(var2, sample_sudoku)])
    return encoding


# Each number can appear exactly once in each hypersquare.
def exactly_one_hypersquare(sample_sudoku):
    return at_least_hypersquare(sample_sudoku) + at_most_hypersquare(sample_sudoku)


def minimal_encoding(names):
    """
    Return the set of clauses corresponding to the minimal encoding.
    """
    encoding = []
    encoding.extend(atleast_cell(names))
    encoding.extend(atmost_row(names))
    encoding.extend(atmost_column(names))
    encoding.extend(atmost_block(names))

    return encoding


def extended_encoding(names):
    """
    Return the set of clauses corresponding to the extended encoding.
    """
    encoding = []
    encoding.extend(exactly_one(names))
    encoding.extend(exactly_one_row(names))
    encoding.extend(exactly_one_column(names))
    encoding.extend(exactly_one_block(names))

    return encoding


def efficient_encoding(names):
    """
    Return the set of clauses corresponding to the efficient encoding.
    """
    encoding = []
    encoding.extend(atleast_cell(names))
    encoding.extend(atmost_cell(names))
    encoding.extend(atmost_row(names))
    encoding.extend(atmost_column(names))
    encoding.extend(atmost_block(names))

    return encoding


def assigned_variables(sample_sudoku):
    """
    Given a sudoku, return a list of the assigned variables.
    """
    assigned = []
    for i in range(9):
        for j in range(9):
            value = sample_sudoku[i][j]
            if value > 0:
                assigned.append([i + 1, j + 1, value])
    return assigned


def same_cell(var_1, var_2):
    """
    Return true if two variables are in the same cell and have different values.
    """
    a, b, c = var_1[0], var_1[1], var_1[2]
    d, e, f = var_2[0], var_2[1], var_2[2]
    if a == d and b == e and c != f:
        return True
    return False


def same_row(var_1, var_2):
    """
    Return true if two variables are in the same row and have the same values.
    """
    a, b, c = var_1[0], var_1[1], var_1[2]
    d, e, f = var_2[0], var_2[1], var_2[2]
    if a == d and b != e and c == f:
        return True
    return False


def same_column(var_1, var_2):
    """
    Return true if two variables are in the same column and have the same values.
    """
    a, b, c = var_1[0], var_1[1], var_1[2]
    d, e, f = var_2[0], var_2[1], var_2[2]
    if a != d and b == e and c == f:
        return True
    return False


def top_left_square(variable, length_of_sudoku):
    """
    Given any index and the length of the sudoku,
    return the index of the top left square in
    the box where it is located.
    """
    top_left = [1,1]
    row, column = variable.copy()[0], variable.copy()[1]
    while (row - sqrt(length_of_sudoku)) > 0:
        row -= sqrt(length_of_sudoku)
        top_left[0] += int(sqrt(length_of_sudoku))
    while (column - sqrt(length_of_sudoku)) > 0:
        column -= sqrt(length_of_sudoku)
        top_left[1] += int(sqrt(length_of_sudoku))
    return top_left


def same_block(var_1, var_2, length_of_sudoku):
    """
    Return true if two variables are in the same block and have the same values.
    """
    if var_1 == var_2:
        return False
    if var_1[2] == var_2[2]:
        if top_left_square(var_1, length_of_sudoku) == top_left_square(var_2, length_of_sudoku):
            return True
    return False


def all_variables(sample_sudoku):
    """
    Return list of all variables needed in a sudoku.
    """
    variable_list = []
    for rows in range(1, len(sample_sudoku[0]) + 1):
            for columns in range(1, len(sample_sudoku[0]) + 1):
                    for values in range(1, len(sample_sudoku[0]) + 1):
                        variable_list.append([rows, columns, values])
    return variable_list


def create_falsehoods(sample_sudoku):
    """
    Return a list of the variables which the assignment renders immediately false.
    """
    variables = all_variables(sample_sudoku)
    falsehoods = []
    for truth in assigned_variables(sample_sudoku):
        for member in variables:
            if same_cell(truth, member):
                falsehoods.append(member)
            if same_row(truth, member):
                falsehoods.append(member)
            if same_column(truth, member):
                falsehoods.append(member)
            if same_block(truth, member, len(sample_sudoku[0])):
                falsehoods.append(member)
    return falsehoods


def encode_into_number(variable, sample_sudoku):
    """
    Friendly indexing.
    """
    row, column, value = variable[0], variable[1], variable[2]
    n = len(sample_sudoku[0])
    return int((row - 1) * (n**2) + (column - 1) * n + value)


def create_hyper_falsehoods(sample_sudoku):
    """
    Return a list of the hypervariables which the assignment renders immediately false.
    """
    variables = all_variables(sample_sudoku)
    falsehoods = []
    for truth in assigned_variables(sample_sudoku):
        for member in variables:
            if same_cell(truth, member):
                falsehoods.append(member)
            if same_row(truth, member):
                falsehoods.append(member)
            if same_column(truth, member):
                falsehoods.append(member)
            if same_block(truth, member, len(sample_sudoku[0])):
                falsehoods.append(member)
            if incompatible_hyperBlock(truth, member, len(sample_sudoku[0])):
                falsehoods.append(member)
    return falsehoods
