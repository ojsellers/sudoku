"""
@author: Ollie
"""

import pygame
from pygame.locals import *
import sys
from SudokuGenerator import *

class gui():
    '''Initialise all variables that define the gui'''
    def __init__(self):
        self.win_size = 130
        self.win_mult = 5
        self.win_ext = 200
        self.win_width = self.win_size * self.win_mult + self.win_ext
        self.win_height = self.win_size * self.win_mult
        self.square_size = int(self.win_size * self.win_mult / 3)
        self.cell = int(self.square_size / 3)
        self.black = (0, 0, 0)
        self.grey = (200, 200, 200)
        self.darker_grey = (160, 160, 160)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.hot_pink = (255,105,180)
        self.blue = (0, 0, 255)
        self.fps = 10
        self.x = self.win_width - self.win_ext + 25
        self.y = 50
        self.w = 150
        self.h = 100
        self.grid = np.zeros((9, 9))

    def draw_lines(self):
        for i in range(0, self.win_width - self.win_ext, self.cell):
            pygame.draw.line(self.display, self.grey,
                             (i, 0), (i, self.win_height))
            pygame.draw.line(self.display, self.grey,
                             (0, i), (self.win_width - self.win_ext, i))
        for j in range(0, self.win_width, self.square_size):
            pygame.draw.line(self.display, self.black,
                             (j, 0), (j, self.win_height))
            pygame.draw.line(self.display, self.black,
                             (0, j), (self.win_width - self.win_ext, j))

    def draw_numbers(self):
        font = pygame.font.SysFont('calibri', 45)
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    number = font.render(str(int(self.grid[i][j])),
                                         False, self.black)
                    num_w = number.get_rect().width
                    num_h = number.get_rect().height
                    self.display.blit(number,
                                      ((self.cell - num_w) / 2 + self.cell * j,
                                       (self.cell - num_h)/ 2 + self.cell * i))
                    pygame.display.update()
                    time.sleep(3 / 81)

    '''A function to draw a simple rectangular pygame button of a desired size
    and location with text on it'''
    def draw_button(self, colour, text, x, y, w, h):
        font = pygame.font.SysFont('calibri', 25, bold = True)
        pygame.draw.rect(self.display, colour, (x, y, w, h))
        textsurface = font.render(text, False, self.blue)
        word_width = textsurface.get_rect().width
        self.display.blit(textsurface, (x + (w - word_width) / 2, y + h / 3))

    '''This function draws the particular buttons for this sudoku generator'''
    def draw_buttons(self):
        names = ['New Easy', 'New Medium', 'New Hard', 'Solve It']
        for i in range(4):
            self.draw_button(self.hot_pink, names[i], self.x,
                             self.y + i * 130, self.w, self.h)

    '''when a mouse click occurs on a button, this function is called and
    performs a routine depending on which button was clicked'''
    def click_funct(self, nums_to_remove, y, method, i):
        self.draw_button(self.green, 'Wait...', self.x,
                         y, self.w, self.h)
        pygame.display.update()
        if method == 'g':
            self.setup()
            new = sudoku_generator(np.zeros((9, 9)))
            new.gen_reasonable_time(nums_to_remove, 0.1)
            self.grid = new.grid
            self.draw_numbers()
        if method == 's':
            new = sudoku_solverAI(self.grid)
            new.solve('single_soln')
            new.update_grid() #added this line for ai
            self.grid = new.grid
            self.draw_numbers()
        self.draw_buttons()

    '''This a function to determine when and where a button click is'''
    def button_click(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            for i in range(4):
                if (self.x + self.w > mouse[0] > self.x and
                    self.y + i * 130 + self.h > mouse[1] > self.y + i * 130):
                    if i == 3:
                        if np.count_nonzero(self.grid != 0) == 0:
                            self.draw_button(self.white, 'Cannot Solve',
                                             self.x, self.y + i * 130,
                                             self.w, self.h)
                            pygame.display.update()
                            time.sleep(2)
                            self.draw_buttons()
                            return
                        self.click_funct(None, self.y + i * 130, 's', i)
                    else:
                        self.click_funct(30 + i * 10 - (i * 2),
                                         self.y + i * 130, 'g', i)
        else:
            return

    '''This function can be called to set up the pygame window'''
    def setup(self):
        self.fpsclock = pygame.time.Clock()
        self.fpsclock.tick(self.fps)
        self.display = pygame.display.set_mode((self.win_width,
                                                self.win_height))
        self.display.fill(self.white)
        pygame.display.set_caption('Sudoku')
        self.draw_lines()
        self.draw_buttons()
