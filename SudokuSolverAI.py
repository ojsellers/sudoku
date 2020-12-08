"""
@author: Ollie
"""

import numpy as np
import copy
import time

class sudoku_solverAI():
    def __init__(self, grid):
        self.grid = grid
        self.solutions = 0
        self.grid_vals = {}
        self.neighbrs = {}
        self.init_dicts()
        self.force_values()


    def init_dicts(self):
        """
        Function to initialise grid_vals dict with pre-determined squares and
        every possible number for empty squares, and initialise a dict for the
        neighbours (share same seq 1-9 rule) of each square to save time later
        """
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.grid_vals.update({str([i, j]): [self.grid[i][j]]})
                
                else:
                    self.grid_vals.update({str([i, j]): [1, 2, 3, 4,
                                                            5, 6, 7, 8, 9]})
        
        return True


    def neighbours(self, i, j, values):
        """
        Returns combined array of in-box and in-line positions for input i, j
        position
        """
        for x in range(0, 9):
            values.append([i, x]), values.append([x, j])
            
        for x in range(0, 3):
            for y in range(0, 3):
                if [(i // 3) * 3 + x, (j // 3) * 3 + y] not in values:
                    values.append([(i // 3) * 3 + x, (j // 3) * 3 + y])
        
        return np.array([value for value in values if value != [i, j]])


    def reduce_grid_vals(self, i, j, n):
        """
        Function takes a position and value input and removes this value from
        the positions neighbours
        """
        neighbours = self.neighbours(i, j, [])
        
        for x in range(len(neighbours)):
            
            index = str(list([int(neighbours[x, 0]), int(neighbours[x, 1])]))
            current = self.grid_vals[index]
            new = [value for value in current if value not in n]
            
            if len(new) == 0:
                return False
            
            self.grid_vals[index] = new
            
            if len(new) == 1 and len(current) == 2:
                self.reduce_grid_vals(neighbours[x, 0], neighbours[x, 1], new)
        
        return True


    def force_values(self):
        """
        Function to input forced values through constraint propagation
        """
        for i in range(9):
            for j in range(9):
                if len(self.grid_vals[str([i, j])]) == 1:
                    if not self.reduce_grid_vals(i, j,
                                                self.grid_vals[str([i, j])]):
                        return False
        return True


    def variable_order(self):
        """
        Function to output the dict key (i) for the position with the lowest
        number of possibilities to decrease number of searches
        """
        for i in sorted(self.grid_vals, key=lambda i: len(self.grid_vals[i])):
            if len(self.grid_vals[i]) >= 2:
                return i
        return False


    def solve(self, method):
        """
        Utilising constraint propagation to solve sudoku with a depth-first
        search, method input can be single solution or not but will be stopped at
        2 solutions for check when generating
        """
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


    def update_grid(self):
        """
        Function to update np array class variable (self.grid) from dict
        """
        for i in range(9):
            for j in range(9):
                if len(self.grid_vals[str([i, j])]) == 1:
                    self.grid[i][j] = int(self.grid_vals[str([i, j])][0])
