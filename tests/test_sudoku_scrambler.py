from src.Sudoku import Sudoku
from src.SudokuScrambler import SudokuScrambler
import pytest
from copy import deepcopy
import numpy as np


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


def test_swap_all_digits(example_sudoku_1):
    assert example_sudoku_1.get_cell(0, 0) == 7
    assert example_sudoku_1.get_cell(3, 1) == 1

    scrambler = SudokuScrambler(example_sudoku_1)
    scrambler.swap_all_digits(7, 1)

    assert example_sudoku_1.get_cell(0, 0) == 1
    assert example_sudoku_1.get_cell(3, 1) == 7


def test_shuffle_rows(example_sudoku_1):
    first_row = deepcopy(example_sudoku_1.get_row(0))

    scrambler = SudokuScrambler(example_sudoku_1)
    scrambler.shuffle_rows([1, 0, 2, 3, 4, 5, 6, 7, 8])

    assert np.array_equal(first_row, example_sudoku_1.get_row(1))


def test_shuffle_cols(example_sudoku_1):
    first_col = deepcopy(example_sudoku_1.get_col(0))

    scrambler = SudokuScrambler(example_sudoku_1)
    scrambler.shuffle_cols([8, 1, 2, 3, 4, 5, 6, 7, 0])
    
    assert np.array_equal(first_col, example_sudoku_1.get_col(8))


def test_remove_digits(example_sudoku_1):
    scrambler = SudokuScrambler(example_sudoku_1)

    assert example_sudoku_1.get_cell(4, 0) == 3

    scrambler.remove_digit(4)
    assert example_sudoku_1.get_cell(4, 0) == 0

