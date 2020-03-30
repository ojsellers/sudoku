"""
@author: Ollie
"""

import time
from SudokuSolver import *
 
class sudoku_generator():
    def __init__(self, grid):
        self.grid = grid
        self.solver = sudoku_solver(self.grid)
     
    '''This function finds a random cell that isn't empty, so the 
        backtracking method can be applied to reduce a full board down to a 
        puzzle of the desired difficulty'''
    def rand_not_empty(self):
        condition = False
        while condition == False:
            ref = np.random.randint(0, 9, (2, 1))
            if self.grid[int(ref[0])][int(ref[1])] != 0:
                condition = True
                return int(ref[0]), int(ref[1])
                
    def remove_number(self):
        i, j = self.rand_not_empty()
        self.grid[i][j] = 0
        
    '''A function to confirm that there is still a unique soln to the puzzle'''
    def check_solutions(self, num_solns):
        self.solver.grid, self.solver.solutions = self.grid, 0
        self.solver.solve('solve')
        self.grid, self.solutions = self.solver.grid, self.solver.solutions
        if self.solutions == num_solns:
            return True
        else:
            return False
    
    '''Another implementation of the backtracking method to reduce a full board
    to a puzzle by removing the desired amount of nummbers. It also contains
    an if statement to end the function if it goes over a certain time limit'''
    def generate(self, nums_to_remove, time0, time_lim):
        if (time.time() - time0) >= time_lim:
            return False
        if np.count_nonzero(self.grid == 0) < nums_to_remove:
            for n in range(np.count_nonzero(self.grid != 0)):
                if (time.time() - time0) >= time_lim:
                    return False
                copy_grid = self.grid
                self.remove_number()
                if self.generate(nums_to_remove, time0, time_lim):
                    if self.check_solutions(1):
                        return True
                self.grid = copy_grid
            return False
        else:
            return True
        
    '''As the backtracking algorithm can be very computationally intensive 
    depending on the random starting point, this function reduces time taken
    to produce a puzzle by enforcing a limit to each attempt'''
    def gen_reasonable_time(self, nums_to_remove, time_lim):
        for i in range(10):
            self.solver.grid = self.grid
            self.solver.solve('builder')
            self.grid = self.solver.grid
            if self.generate(nums_to_remove, time.time(), time_lim):
                return True
        print("Too long - try again")
        self.grid = np.zeros((9, 9))
        return False
