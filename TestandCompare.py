import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from SudokuSolverAI import *
from SudokuSolver import *

'''Use sudoku csv containing 1,000,000 puzzles from kaggle'''
sudokus = pd.read_csv("/home/ollie/sudoku/sudoku.csv")

def TestSolveTime(n):
    times = []
    timesAI = []
    num_zeros = []

    start_point = np.random.randint(0, 1000000 - n)

    for i in range(n):
        puzzle = np.array(list(map(list, zip(*[map(int,
                                sudokus.loc[i + start_point][0])] * 9))))
        num_zeros.append(np.count_nonzero(puzzle == 0))
        soln = np.array(list(map(list, zip(*[map(int,
                                sudokus.loc[i + start_point][1])] * 9))))

        toc = time.time()
        solver = sudoku_solver(puzzle)
        solver.solve('single_soln')
        assert(solver.grid.all() == soln.all())
        assert(solver.solutions == 1)
        times.append(time.time() - toc)

        tic = time.time()
        solverAI = sudoku_solverAI(puzzle)
        solverAI.solve('single_soln')
        solverAI.update_grid()
        assert(solverAI.grid.all() == soln.all())
        assert(solverAI.solutions == 1)
        timesAI.append(time.time() - tic)

    return times, timesAI, num_zeros

times, timesAI, num_zeros = TestSolveTime(1000)

plt.scatter(num_zeros, times, label='backtracking')
plt.scatter(num_zeros, timesAI, label='const prop')
plt.xlabel('Number of zeros in starting grid')
plt.ylabel('Time (s)')
plt.legend()
plt.show()

print("Average backtracking time:", np.average(times))
print("Average constraint propagation time:", np.average(timesAI))
