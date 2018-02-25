import collections
from utils import *


class SudokuAgent:
    """
     This agent find the solution to a Sudoku puzzle using search and constraint propagation
    """

    def __init__(self, sudoku):
        self.m_sudoku = sudoku
        self.m_possible_result = None
        self.m_result_history = None

    def solve(self):
        self.m_possible_result = self.__search(self.m_sudoku)
        debug_display(self.m_possible_result)

    def __search(self, sudoku):
        """
        Apply depth first search to solve Sudoku puzzles in order to solve puzzles
        that cannot be solved by repeated reduction alone.
        """
        print "__search"
        debug_display(sudoku)
        sudoku = self.__simplify(sudoku)
        if sudoku is None:
            return None  # Failed
        if sudoku.is_complete():
            return sudoku  # Success

        # Choose one of the unfilled squares with the fewest possibilities
        x, y = self.__next_min_solvable_value(sudoku)
        # Now use recurrence to solve each one of the resulting sudokus
        for possible_value in sudoku.get_possible_values(x, y):
            new_sudoku = sudoku.deepcopy()
            new_sudoku.update_value(x, y, possible_value)
            new_sudoku = self.__search(new_sudoku)
            if new_sudoku is not None:
                return new_sudoku

    def __next_min_solvable_value(self, sudoku):
        min_val = 10
        min_x, min_y = 0, 0
        values = sudoku.get_values()
        for x in range(len(values)):
            for y in range(len(values[0])):
                if len(values[x][y]) > 1 and min_val > len(sudoku.get_possible_values(x, y)):
                    min_val = len(sudoku.get_possible_values(x, y))
                    min_x, min_y = x, y
        return min_x, min_y

    def __simplify(self, sudoku):
        """
        Iterate available algos i.e. eliminate() and only_choice() to simplify.
        If at some point, there is a box with no available values, return False.
        If the game is solved, return the game.
        If after an iteration of both functions, the game remains the same, return the game.
        Input: A game in dictionary form.
        Output: The resulting game in dictionary form.
        """
        is_state_simplified = 1
        while is_state_simplified is not 0:
            solved_values_before = self.__solved_values(sudoku)
            self.__eliminate(sudoku)
            values = self.__only_choice(sudoku)
            solved_values_after = self.__solved_values(sudoku)
            is_state_simplified = cmp(solved_values_before, solved_values_after)
            # If reached invalid state
            if not sudoku.is_valid():
                return None
        return sudoku

    def __solved_values(self, sudoku):
        solved_values = []
        values = sudoku.get_values()
        for x in range(len(values)):
            for y in range(len(values[0])):
                if len(sudoku.get_possible_values(x, y)) == 1:
                    solved_values.append(sudoku.get_possible_values(x, y)[0])
        solved_values.sort()
        return solved_values

    def __eliminate(self, sudoku):
        """
        Go through all the boxes, and whenever there is a box with a value, eliminate this value
        from the values of all its peers.
        Input: A game in dictionary form.
        Output: The resulting game in dictionary form.
        """
        is_state_simplified = 1
        while is_state_simplified is not 0:
            solved_values_before = self.__solved_values(sudoku)
            # eliminate
            values = sudoku.get_values()
            for x in range(len(values)):
                for y in range(len(values[0])):
                    possible_values = sudoku.get_possible_values(x, y)
                    if len(possible_values) == 1:
                        sudoku.update_possible_values(x, y, possible_values[0])

            solved_values_after = self.__solved_values(sudoku)
            is_state_simplified = cmp(solved_values_before, solved_values_after)
            # If reached invalid state
            if not sudoku.is_valid():
                return None
        return sudoku

    def __only_choice(self, sudoku):
        """
        Go through all the units, and whenever there is a unit with a value that only fits
        in one box, assign the value to this box.
        Input: A game in dictionary form.
        Output: The resulting game in dictionary form.
        """
        values = sudoku.get_values()
        # row
        for x in range(len(values)):
            # check
            options = []
            for y in range(len(values[0])):
                possible_values = sudoku.get_possible_values(x, y)
                if len(possible_values) != 1:
                    options += possible_values
            ctr = collections.Counter(options)
            for key in ctr:
                if ctr[key] == 1:
                    for y in range(len(values[0])):
                        if key in sudoku.get_possible_values(x, y):
                            sudoku.update_value(x, y, key)
                            break
        # col
        for y in range(len(values[0])):
            # check
            options = []
            for x in range(len(values)):
                possible_values = sudoku.get_possible_values(x, y)
                if len(possible_values) != 1:
                    options += possible_values
            ctr = collections.Counter(options)
            for key in ctr:
                if ctr[key] == 1:
                    for x in range(len(values)):
                        if key in sudoku.get_possible_values(x, y):
                            sudoku.update_value(x, y, key)
                            break
        # box
        for box in range(9):
            x, y = (box % 3) * 3, (box // 3) * 3
            options = []
            for idx_x in range(3):
                for idx_y in range(3):
                    possible_values = sudoku.get_possible_values(x + idx_x, y + idx_y)
                    if len(possible_values) != 1:
                        options += possible_values
            ctr = collections.Counter(options)
            for key in ctr:
                if ctr[key] == 1:
                    for idx_x in range(3):
                        for idx_y in range(3):
                            if key in sudoku.get_possible_values(x + idx_x, y + idx_y):
                                sudoku.update_value(x + idx_x, y + idx_y, key)
                                break
        return sudoku
