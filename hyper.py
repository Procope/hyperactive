import numpy as np
import pycosat
import subprocess
import tempfile
from encoder import create_sudoku_vars, minimal_encoding, extended_encoding, efficient_encoding, to_cnf_string, to_cnf_file, optimised_encoding, exactly_one_hypersquare


def get_data(filename, n_sudokus=100):
    quizzes = np.zeros((n_sudokus, 81), np.int32)

    for i, line in enumerate(open(filename, 'r').read().splitlines()):
        if i >= n_sudokus:
            break;

        quizzes[i] = list(map(int,line.split(",")))
    return quizzes.reshape((-1, 9, 9))

def solution_to_array(cnf_solution, indices):
    sol_array = np.zeros((9,9), dtype=np.int)
    for literal in cnf_solution:
            if literal > 0:
                (i, j, k) = indices[literal]
                sol_array[i-1][j-1] = k
    return sol_array


if __name__ == "__main__":
    n_samples = 10

    quizzes = get_data('/Users/mario/Documents/Uni/WS1718/KR/data/hyper.txt', n_samples)

    print("Shape of quizzes:", quizzes.shape)

    names, indices = create_sudoku_vars(n = 9)

    min_encoding = minimal_encoding(names)
    eff_encoding = efficient_encoding(names)
    ext_encoding = extended_encoding(names)

    zchaff_overall_stats = list()
    walksat_overall_stats = list()

    for idx, quiz in enumerate(quizzes):
        print(idx, "quizzes solved.")

        # opt_encod_cnf = to_cnf_string(optimised_encoding(ext_encoding, quiz))
        # to_cnf_file(optimised_encoding(ext_encoding, quiz), 'opt2.cnf')
        # print(optimised_encoding(ext_encoding, quiz))

        min_encoding.extend(exactly_one_hypersquare(quiz))
        eff_encoding.extend(exactly_one_hypersquare(quiz))
        ext_encoding.extend(exactly_one_hypersquare(quiz))

        encodings = [e.copy() for e in [min_encoding, eff_encoding, ext_encoding]]

#         pycosat_solution = pycosat.solve(optimised_encoding(ext_encoding, quiz))
#         sol_array = solution_to_array(pycosat_solution, indices)
#         print(solutions)

        for i in range(9):
            for j in range(9):
                value = quiz[i][j]
                if value > 0:
                    pos_literal = [int(names[i, j, value - 1])]
                    for e in encodings:
                        e.append(pos_literal)

        min_encod_cnf = to_cnf_string(encodings[0])
        eff_encod_cnf = to_cnf_string(encodings[1])
        ext_encod_cnf = to_cnf_string(encodings[2])


        for i, e in enumerate([min_encod_cnf, eff_encod_cnf, ext_encod_cnf]):
        # for i, e in enumerate([opt_encod_cnf]):
            tmp = tempfile.NamedTemporaryFile()
            tmp.write(e.encode('utf-8'))

            zchaff_result = subprocess.run(['../zchaff64/zchaff', tmp.name], stdout=subprocess.PIPE)
            zchaff_stats = zchaff_result.stdout.decode('utf-8')

            walksat_result = subprocess.run(['../Walksat_v51/walksat', '-best', tmp.name], stdout=subprocess.PIPE)
            walksat_stats = walksat_result.stdout.decode('utf-8')

            tmp.close()

            begin_zchaff_solution = zchaff_stats.find('Instance Satisfiable\n') + len('Instance Satisfiable\n')
            end_zchaff_solution = zchaff_stats.find('Random Seed') - 1
            zchaff_cnf_solution = list(map(int, zchaff_stats[begin_zchaff_solution: end_zchaff_solution].split(' ')))

            begin_zchaff_stats = zchaff_stats.find('Max Decision Level')
            zchaff_stats_list = zchaff_stats[begin_zchaff_stats:].replace('\t', ' ').replace('  ', '    ').replace('\n', '    ').split("    ")
            zchaff_stats_list = [x for x in zchaff_stats_list if x != '']

            begin_walksat_stats = walksat_stats.find('total elapsed seconds')
            end_walksat_stats = max(walksat_stats.find('ASSIGNMENT FOUND'), walksat_stats.find('final numbad level statistics')) - 1

            if end_walksat_stats < 0:
                print(walksat_stats)
            walksat_stats_list = [x.split("=") for x in walksat_stats[begin_walksat_stats:end_walksat_stats].split("\n")]

            zchaff_stats_dict = {}
            for j in range(0, len(zchaff_stats_list)-1, 2):
                if zchaff_stats_list[j] == '( Stack + Vsids + Shrinking Decisions )':
                    continue
                zchaff_stats_dict[zchaff_stats_list[j]] = zchaff_stats_list[j+1]

            for stat, value in zchaff_stats_dict.items():
                try:
                    zchaff_overall_stats[i][stat] += float(value)
                except IndexError:
                    zchaff_overall_stats.append(dict())
                    zchaff_overall_stats[i][stat] = float(value)
                except KeyError:
                    zchaff_overall_stats[i][stat] = float(value)

            # # WALKSAT
            for key_value in walksat_stats_list:
                if len(key_value) != 2:
                    continue

                stat = key_value[0].strip()
                value = key_value[1].strip()
                try:
                    walksat_overall_stats[i][stat] += float(value)
                except IndexError:
                    walksat_overall_stats.append(dict())
                    walksat_overall_stats[i][stat] = float(value)
                except KeyError:
                    walksat_overall_stats[i][stat] = float(value)

    print('\n\nZchaff with (1) minimal encoding, (2) efficient encoding, (3) extended encoding, (4) optimised encoding \n')
    for j, stats in enumerate(zchaff_overall_stats):
        print("Encoding ({})".format(j+1))
        for key in stats.keys():
            print(key, stats[key]/n_samples)
        print()

    print('Walksat with (1) minimal encoding, (2) efficient encoding, (3) extended encoding, (4) optimised encoding \n')
    for j, stats in enumerate(walksat_overall_stats):
        print("Encoding ({})".format(j+1))
        for key in stats.keys():
            print(key, stats[key]/n_samples)
        print()



        # pycosat_solution = pycosat.solve(optimised_encoding(ext_encoding, quiz))
        # sol_array = solution_to_array(pycosat_solution, indices)
        # print(solutions)
        # if not np.array_equal(sol_array, solutions[idx]):
        #     print('Original solution:')
        #     print(solutions[idx])
        #     print('SAT solution:')
        #     print(sol_array)
