import pygame
from pygame.locals import *
from utils import *


class SudokuGame:
    def __init__(self, sudoku):
        self.m_sudoku = sudoku

        # Set up couple of class constants, used for rendering
        # Sets size of grid
        self.WINDOW_MULTIPLIER = 5  # Modify this number to change size of grid
        self.WINDOW_SIZE = 81
        self.WINDOW_WIDTH = self.WINDOW_SIZE * self.WINDOW_MULTIPLIER
        self.WINDOW_HEIGHT = self.WINDOW_SIZE * self.WINDOW_MULTIPLIER
        self.SQUARE_SIZE = (self.WINDOW_SIZE * self.WINDOW_MULTIPLIER) // 3
        self.CELL_SIZE = self.SQUARE_SIZE // 3
        self.NUMBER_SIZE = self.CELL_SIZE // 3  # Position of unsolved number

        self.FONT_STYLE = 'freesansbold.ttf'
        self.BASIC_FONT_SIZE = 12
        self.LARGE_FONT_SIZE = 55
        self.FPS = 64

        # Set up the colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.LIGHT_GRAY = (200, 200, 200)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        pygame.init()
        self.FPS_CLOCK = pygame.time.Clock()
        self.DISPLAY_SURFACE = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.BASIC_FONT = pygame.font.Font(self.FONT_STYLE, self.BASIC_FONT_SIZE)
        self.LARGE_FONT = pygame.font.Font(self.FONT_STYLE, self.LARGE_FONT_SIZE)

    def play(self):
        self.__update_board()
        pygame.display.update()
        while True:  # main game loop
            pygame.event.pump()
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.display.quit()
                return
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                print mouse_x
                print mouse_y
                self.__select_cell(mouse_x, mouse_y)
                pygame.display.update()
            self.FPS_CLOCK.tick(self.FPS)

    def __update_board(self):
        """
        This function draws grid lines on the Sudoku box
        """
        self.DISPLAY_SURFACE.fill(self.WHITE)
        # Draw Minor Lines
        for x in range(0, self.WINDOW_WIDTH, self.CELL_SIZE):  # draw vertical lines
            if x % (3 * self.CELL_SIZE) != 0:
                pygame.draw.line(self.DISPLAY_SURFACE, self.LIGHT_GRAY, (x, 0), (x, self.WINDOW_HEIGHT))
        for y in range(0, self.WINDOW_HEIGHT, self.CELL_SIZE):  # draw horizontal lines
            if y % (3 * self.CELL_SIZE) != 0:
                pygame.draw.line(self.DISPLAY_SURFACE, self.LIGHT_GRAY, (0, y), (self.WINDOW_WIDTH, y))
        # Draw Major Lines
        for x in range(0, self.WINDOW_WIDTH, self.SQUARE_SIZE):  # draw vertical lines
            pygame.draw.line(self.DISPLAY_SURFACE, self.BLACK, (x, 0), (x, self.WINDOW_HEIGHT))
        for y in range(0, self.WINDOW_HEIGHT, self.SQUARE_SIZE):  # draw horizontal lines
            pygame.draw.line(self.DISPLAY_SURFACE, self.BLACK, (0, y), (self.WINDOW_WIDTH, y))
        # Initialize the values in board
        self.__display_cells(self.m_sudoku.get_values(), self.BLACK, self.LIGHT_GRAY)

    def __display_cells(self, current_grid, color1, color2):
        """
        Displays the cells with the values assigned to them, and specify the color
        """
        for x in range(len(current_grid)):  # item is x,y co-ordinate from 0 - 8
            row = current_grid[x]
            for y in range(len(row)):  # iterates through each number
                item = str(row[y])
                if len(item) == 1:
                    self.__populate_cell(item, x * self.CELL_SIZE, y * self.CELL_SIZE, self.LARGE_FONT, color1)
                else:
                    self.__fill_cell(x * self.CELL_SIZE, y * self.CELL_SIZE, self.BASIC_FONT, color2)

    def __populate_cell(self, cell_data, x, y, font, color):
        """
        Writes cell data at given x, y co-ordinates
        """
        cell_surf = font.render('%s' % (cell_data), True, color)
        cell_rect = cell_surf.get_rect()
        cell_rect.topleft = (x + 5, y)
        self.DISPLAY_SURFACE.blit(cell_surf, cell_rect)

    def __fill_cell(self, x, y, font, color):
        for idx in range(3):
            for idy in range(3):
                item = idx + idy * 3 + 1
                self.__populate_cell(item, x + idx * self.NUMBER_SIZE, y + idy * self.NUMBER_SIZE, font, color)

    def __select_cell(self, x, y):
        cell_x, cell_y = x // self.CELL_SIZE, y // self.CELL_SIZE
        if len(str(self.m_sudoku.get_values()[cell_x][cell_y])) != 1:
            number_x, number_y = (x - cell_x * self.CELL_SIZE) // self.NUMBER_SIZE, (
                y - cell_y * self.CELL_SIZE) // self.NUMBER_SIZE
            item = number_x + number_y * 3 + 1
            self.m_sudoku.update_value(cell_x, cell_y, item)
            self.__update_board()
