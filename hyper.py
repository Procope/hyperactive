import numpy as np

import pycosat

import subprocess
import tempfile
import argparse

from encoder import create_sudoku_vars, minimal_encoding, extended_encoding, efficient_encoding, to_cnf_string, exactly_one_hypersquare


def get_data(filename, n_sudokus=100):
    """
    Load Hyper Sudokus from data set (as a list of matrices).
    """
    quizzes = np.zeros((n_sudokus, 81), np.int32)

    for i, line in enumerate(open(filename, 'r').read().splitlines()):
        if i >= n_sudokus:
            break;

        quizzes[i] = list(map(int,line.split(",")))
    return quizzes.reshape((-1, 9, 9))


def decode_solution(cnf_solution, indices):
    """
    Decode a DIMACS solution into a sudoku matrix.
    """
    sol_array = np.zeros((9,9), dtype=np.int)
    for literal in cnf_solution:
            if literal > 0:
                (i, j, k) = indices[literal]
                sol_array[i-1][j-1] = k
    return sol_array


if __name__ == "__main__":
    parser = argparse.ArgumentParser("hyper")
    parser.add_argument("path", type=str)
    parser.add_argument("num_sudokus", type=int)
    parser.add_argument("variant", help="best, novelty, rnovelty", type=str)

    args = parser.parse_args()

    quizzes = get_data(args.path, args.num_sudokus)
    print("Shape of quizzes:", quizzes.shape)

    names, indices = create_sudoku_vars(n = 9)

    min_encoding = minimal_encoding(names)
    eff_encoding = efficient_encoding(names)
    ext_encoding = extended_encoding(names)

    zchaff_overall_stats = list()
    walksat_overall_stats = list()

    for idx, quiz in enumerate(quizzes):
        min_encoding.extend(exactly_one_hypersquare(quiz))
        eff_encoding.extend(exactly_one_hypersquare(quiz))
        ext_encoding.extend(exactly_one_hypersquare(quiz))

        encodings = [e.copy() for e in [min_encoding, eff_encoding, ext_encoding]]

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
            tmp = tempfile.NamedTemporaryFile()
            tmp.write(e.encode('utf-8'))

            # write zChaff result to temporary file
            zchaff_result = subprocess.run(['../zchaff64/zchaff', tmp.name], stdout=subprocess.PIPE)
            zchaff_stats = zchaff_result.stdout.decode('utf-8')

            # write WalkSAT result to temporary file
            walksat_result = subprocess.run(['../Walksat_v51/walksat', '-' + args.variant, tmp.name], stdout=subprocess.PIPE)
            walksat_stats = walksat_result.stdout.decode('utf-8')

            tmp.close()

            #
            # Parse results.
            #
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

            # zChaff stats
            zchaff_stats_dict = {}
            for j in range(0, len(zchaff_stats_list)-1, 2):
                if zchaff_stats_list[j] == '( Stack + Vsids + Shrinking Decisions )':
                    continue
                zchaff_stats_dict[zchaff_stats_list[j]] = zchaff_stats_list[j+1]

            for stat, value in zchaff_stats_dict.items():
                try:
                    zchaff_overall_stats[i][stat].append(float(value))
                except IndexError:
                    zchaff_overall_stats.append(dict())
                    zchaff_overall_stats[i][stat] = [float(value)]
                except KeyError:
                    zchaff_overall_stats[i][stat] = [float(value)]

            # WalkSAT stats
            for key_value in walksat_stats_list:
                if len(key_value) != 2:
                    continue

                stat = key_value[0].strip()
                value = key_value[1].strip()
                try:
                    walksat_overall_stats[i][stat].append(float(value))
                except IndexError:
                    walksat_overall_stats.append(dict())
                    walksat_overall_stats[i][stat] = [float(value)]
                except KeyError:
                    walksat_overall_stats[i][stat] = [float(value)]

        if idx >= 10 and idx % 10 == 0:
            print(idx + 1, "quizzes solved.")

    #
    # Print statistics to standard output.
    #
    print('\n\nZchaff with (1) minimal encoding, (2) efficient encoding, (3) extended encoding\n')
    for j, stats in enumerate(zchaff_overall_stats):
        print("Encoding ({})".format(j+1))
        for key in stats.keys():
            values = np.array(stats[key])
            print(key)
            print("  Mean : {}".format(values.mean()))
            print("  Standard deviation: {}".format(values.std(ddof=1)))
        print()

    print('Walksat with (1) minimal encoding, (2) efficient encoding, (3) extended encoding\n')
    for j, stats in enumerate(walksat_overall_stats):
        print("Encoding ({})".format(j+1))
        for key in stats.keys():
            values = np.array(stats[key])
            print(key)
            print("  Mean : {}".format(values.mean()))
            print("  Standard deviation: {}".format(values.std(ddof=1)))
        print()
