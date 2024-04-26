import pytest
from src.Sudoku import Sudoku
import numpy as np


@pytest.fixture
def example_grid():
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    return grid


@pytest.fixture
def example_string_grid():
    grid = """
        530070000
        600195000
        098000060
        800060003
        400803001
        700020006
        060000280
        000419005
        000080079"""

    return grid


@pytest.fixture
def solved_sudoku():
    grid = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
    sudoku = Sudoku(grid)
    return sudoku


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


def test_constuctor_list(example_grid):
    sudoku = Sudoku(example_grid)
    assert np.array_equal(sudoku.grid, example_grid)


def test_constructor_string(example_grid, example_string_grid):
    sudoku = Sudoku(example_string_grid)
    assert np.array_equal(sudoku.grid, example_grid)


@pytest.mark.xfail(reason="Program exits on invalid grid size")
def test_invalid_size():
    str_grid = """
                111
                222"""

    sudoku = Sudoku(str_grid)


def test_getting_cell(example_sudoku_1):
    cell = example_sudoku_1.get_cell(0, 0)
    assert cell == 7

    cell = example_sudoku_1.get_cell(4, 0)
    assert cell == 3

    cell = example_sudoku_1.get_cell(0, 3)
    assert cell == 5

    cell = example_sudoku_1.get_cell(11, 1)
    assert cell == -1


def test_setting_cell(example_sudoku_1):
    example_sudoku_1.set_cell(1, 0, 5)
    cell = example_sudoku_1.get_cell(1, 0)
    assert cell == 5

    example_sudoku_1.set_cell(0, 0, 8)
    cell = example_sudoku_1.get_cell(0, 0)
    assert cell == 7


def test_is_solved_1(solved_sudoku):
    assert solved_sudoku.is_solved()


def test_is_solved_2(example_sudoku_1):
    assert not example_sudoku_1.is_solved()


def test_get_column(example_sudoku_1):
    column = [7, 0, 3, 5, 2, 0, 0, 0, 0]
    result = example_sudoku_1.get_col(0)
    assert np.array_equal(column, result)


def test_get_row(example_sudoku_1):
    row = [7, 0, 0, 0, 3, 6, 0, 4, 0]
    result = example_sudoku_1.get_row(0)
    assert np.array_equal(row, result)


def test_get_square(example_sudoku_1):
    square = [[0, 0, 0],
              [6, 4, 0], 
              [9, 7, 0]]
    result = example_sudoku_1.get_square(4)
    assert np.array_equal(square, result)

def test_reset_sudoku(example_sudoku_1):
    original_value = example_sudoku_1.get_cell(2, 0) 
    example_sudoku_1.set_cell(2, 0, 5) 
    assert example_sudoku_1.get_cell(2, 0) == 5

    example_sudoku_1.reset_sudoku()
    assert example_sudoku_1.get_cell(2, 0) == 0


def test_clean_cell(example_sudoku_1):
    example_sudoku_1.set_cell(2, 0, 5)
    example_sudoku_1.clean_cell(2, 0)
    assert example_sudoku_1.get_cell(2, 0) == 0


def test_check_rows(solved_sudoku):
    assert solved_sudoku.check_rows()

    solved_sudoku.grid[0][0] = 9
    assert not solved_sudoku.check_rows()


def test_check_cols(solved_sudoku):
    assert solved_sudoku.check_cols()

    solved_sudoku.grid[0][0] = solved_sudoku.grid[1][0]
    assert not solved_sudoku.check_cols()


def test_check_squares(solved_sudoku):
    assert solved_sudoku.check_squares()
    solved_sudoku.grid[1][1] = solved_sudoku.grid[2][2]
    assert not solved_sudoku.check_squares()


def test_string_to_grid():
    input_str = "123456789" * 9
    sudoku = Sudoku(input_str)
    expected_grid = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(9)])
    assert np.array_equal(sudoku.grid, expected_grid)


@pytest.mark.xfail(reason="Program exits on invalid grid shape")
def test_invalid_grid_shape():
    grid = np.zeros((10, 10))  # Invalid shape
    sudoku = Sudoku(grid)


def test_valid_coords():
    assert Sudoku.valid_coords(0, 0)
    assert Sudoku.valid_coords(8, 8)

    assert not Sudoku.valid_coords(-1, 0)
    assert not Sudoku.valid_coords(0, 9)


def test_valid_value():
    assert Sudoku.valid_value(0)
    assert Sudoku.valid_value(9)

    assert not Sudoku.valid_value(10)
    assert not Sudoku.valid_value(-1)