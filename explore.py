import numpy as np
quizzes = np.zeros((1000000, 81), np.int32)
solutions = np.zeros((1000000, 81), np.int32)
for i, line in enumerate(open('/Users/mario/Documents/Uni/WS1718/KR/data/sudoku.csv', 'r').read().splitlines()[1:]):

    quiz, solution = line.split(",")
    for j, q_s in enumerate(zip(quiz, solution)):
        q, s = q_s
        quizzes[i, j] = q
        solutions[i, j] = s

    if i > 2:
        break;

quizzes = quizzes.reshape((-1, 9, 9))
solutions = solutions.reshape((-1, 9, 9))



print(quizzes[0])

print(solutions[0])

