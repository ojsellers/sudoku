"""
@author: Ollie
"""

import numpy as np

class sudoku_solver():
    def __init__(self, grid):
        self.grid = grid
        self.solutions = 0

    def check_line(self, i, j, n):
        for x in range(0, 9):
            if self.grid[i][x] == n or self.grid[x][j] == n:
                return False
        return True
    
    def check_box(self, i , j, n):
        i0 = (i // 3) * 3
        j0 = (j // 3) * 3
        for x in range(0, 3):
            for y in range(0, 3):
                if self.grid[i0 + x][j0 + y] == n:
                    return False
        return True
    
    def possible(self, i, j, n):
        if self.check_box(i, j, n) and self.check_line(i, j, n):
            return True
        return False
    
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
                else:
                    False
          
    '''Implementing a recursive backtracking method to solve the sudoku puzzle,
    generalised for use on single and multiple solution boards. The single_soln 
    method finds a single solution and is also used to generate a full unique 
    board'''
    def solve(self, method):
        if self.find_empty():
            i, j = self.find_empty()
            nums = np.arange(1, 10)
            np.random.shuffle(nums)
            for n in range(9):
                if self.possible(i, j, nums[n]):
                    self.grid[i][j] = nums[n]
                    if method == 'single_soln':
                        if self.solve(method):
                            return True
                    else:
                        self.solve(method)
                    self.grid[i][j] = 0 
            return False
        else:
            self.solutions += 1
            return True
