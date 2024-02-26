import sys

sys.path.insert(0, "..")

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

@pytest.fixture
def easy_sudoku():
    grid = """800000000
        003600000
        070090200
        050007000
        000045700
        000100030
        001000068
        008500010
        090000400"""
    sudoku = Sudoku(grid)
    return sudoku

@pytest.fixture
def unsolvable_sudoku():
    grid = """700036040
        046100070
        389000100
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

def test_is_solvable_1(unsolvable_sudoku):
    solver = SudokuSolver(unsolvable_sudoku)
    assert not solver.is_solvable()

def test_is_solvable_2(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)
    assert solver.is_solvable()

def test_get_first(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)
    result = solver.get_first_empty()
    assert result == (1, 0)

def test_solve(easy_sudoku):
    solver = SudokuSolver(easy_sudoku)
    result = solver.solve()

    assert result is not None


