"""
@author: Ollie
"""

import numpy as np
import copy

class sudoku_solver():
    def __init__(self, grid):
        self.grid = grid
        self.solutions = 0
        self.grid_vals = {}
        self.neighbrs = {}
        self.init_dicts()
        self.force_values()

    '''Function to initialise grid_vals dict with pre-determined squares and
    every possible number for empty squares, and initialise a dict for the
    neighbours (share same seq 1-9 rule) of each square to save time later'''
    def init_dicts(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.grid_vals.update({str([i, j]): [self.grid[i][j]]})
                else:
                    self.grid_vals.update({str([i, j]): [1, 2, 3, 4,
                                                            5, 6, 7, 8, 9]})
                self.neighbrs.update({str([i, j]): self.neighbours(i, j)})
        return True

    '''Returns array of indexes for positions in the same line as input i, j
    position'''
    def line(self, i, j, values):
        for x in range(0, 9):
            values.append([i, x]), values.append([x, j])
        return values

    '''Returns array of indexes for positions in the same local box as input
    i, j position '''
    def box(self, i, j, values):
        for x in range(0, 3):
            for y in range(0, 3):
                values.append([(i // 3) * 3 + x, (j // 3) * 3 + y])
        return values

    '''Returns combined array of in-box and in-line positions for input i, j
    position '''
    def neighbours(self, i, j):
        return np.unique([value for value in (self.line(i, j, []) +
                            self.box(i, j, [])) if value != [i, j]], axis = 0)

    '''Function takes a position and value input and removes this value from
    the positions neighbours'''
    def reduce_grid_vals(self, i, j, n):
        for x in range(len(self.neighbrs[str([i, j])])):
            current = self.grid_vals[str([self.neighbrs[str([i, j])][x,0],
                                            self.neighbrs[str([i, j])][x,1]])]
            new = [value for value in current if value not in n]
            if len(new) == 0:
                return False
            self.grid_vals.update({str([self.neighbrs[str([i, j])][x,0],
                                        self.neighbrs[str([i, j])][x,1]]): new})
            if len(new) == 1 and len(current) == 2:
                self.reduce_grid_vals(self.neighbrs[str([i, j])][x,0],
                                        self.neighbrs[str([i, j])][x,1], new)
        return True

    '''Function to input forced values through constraint propagation'''
    def force_values(self):
        for i in range(9):
            for j in range(9):
                if len(self.grid_vals[str([i, j])]) == 1:
                    if not self.reduce_grid_vals(i, j,
                                                self.grid_vals[str([i, j])]):
                        return False
        return True

    '''Function to output the dict key (i) for the position with the lowest
    number of possibilities to decrease number of searches'''
    def variable_order(self):
        for i in sorted(self.grid_vals, key=lambda i: len(self.grid_vals[i])):
            if len(self.grid_vals[i]) >= 2:
                return i
        return False

    '''Utilising constraint propagation to solve sudoku with a depth-first
    search, method input can be single solution or not but will be stopped at
    2 solutions for check when generating'''
    def solve(self, method):
        if self.solutions >= 2:
            return True
        if self.variable_order():
            i = self.variable_order()
            nums = self.grid_vals[str(self.variable_order())]
            np.random.shuffle(nums)
            for n in range(len(nums)):
                copy_grid_vals = copy.deepcopy(self.grid_vals)
                self.grid_vals.update({str(i): [nums[n]]})
                if self.force_values():
                    if method == 'single_soln':
                        if self.solve(method):
                            self.update_grid()
                            return True
                    else:
                        self.solve(method)
                self.grid_vals = copy_grid_vals
            return False
        else:
            self.solutions += 1
            return True

    '''Function to update np array class variable (self.grid) from dict'''
    def update_grid(self):
        for i in range(9):
            for j in range(9):
                if len(self.grid_vals[str([i, j])]) == 1:
                    self.grid[i][j] = int(self.grid_vals[str([i, j])][0])
