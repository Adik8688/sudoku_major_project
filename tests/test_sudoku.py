import pytest
from src.Sudoku import Sudoku

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
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
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
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
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
    assert sudoku.grid == example_grid


def test_constructor_string(example_grid, example_string_grid):  
    sudoku = Sudoku(example_string_grid)
    assert sudoku.grid == example_grid

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