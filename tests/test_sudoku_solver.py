from code.SudokuSolver import SudokuSolver
from code.Sudoku import Sudoku
import pytest

@pytest.fixture
def example_sudoku_1():
    grid = """700036040
        040100070
        300000100
        530000000
        209640000
        060970080
        020704005
        000008004
        054069001"""
    sudoku = Sudoku(grid)
    return sudoku

def test_possible_values_for_cell(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)

    result = solver.get_list_of_possibilities_for_cell(0, 0)
    assert result == [-1]

    result = solver.get_list_of_possibilities_for_cell(0, 1)
    assert result == [6, 8, 9]

    result = solver.get_list_of_possibilities_for_cell(8, 0)
    assert result == [2, 8, 9]


