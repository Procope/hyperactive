#
# This file is just a draft of the optimised encoding.
#

#function which, given an encoding and a sudoku, outputs a trimmed down list of clauses.
#The 'reduction operators' from the paper are basically contained within the if clauses in the function body.
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

new_encoding = optimised_encoding(encoding, s_test)
print("Number of clauses in old encoding:", len(encoding))
print("Number of clauses in new encoding:", len(new_encoding))
def variable_counter(encoding):
   counter = set()
   for clause in encoding:
       for literal in clause:
           counter.add(literal**2)
   return len(counter)
#
print("Number of variables in old encoding:", variable_counter(encoding))
print("Number of variables in new encoding:", variable_counter(new_encoding))
