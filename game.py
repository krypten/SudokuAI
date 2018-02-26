from game.sudoku import Sudoku
from game.sudoku_agent import SudokuAgent
from game.sudoku_game import SudokuGame
from utils import *

if __name__ == "__main__":
    sudoku_grid_str = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    sudoku_grid = values2grid(sudoku_grid_str)
    print sudoku_grid
    sudoku = Sudoku(sudoku_grid)
    debug_display(sudoku)

    solved_sudoku = SudokuAgent(sudoku.deepcopy()).solve()
    SudokuGame(sudoku.deepcopy(), solved_sudoku.deepcopy()).play()
