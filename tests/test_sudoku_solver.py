from src.SudokuSolver import SudokuSolver
from src.Sudoku import Sudoku
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
    grid = """178000204
    930000050
    000370100
    401000300
    000516000
    002000906
    007068000
    050000083
    809000000"""
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

@pytest.fixture
def hard_sudoku():
    grid = """000801000
    000000043
    500000000
    000070800
    000000100
    020030000
    600000075
    003400000
    000200600"""
    sudoku = Sudoku(grid)
    return sudoku

def test_possible_values_for_cell(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)

    result = solver.get_list_of_candidates_for_cell(0, 0)
    assert result == [-1]

    result = solver.get_list_of_candidates_for_cell(0, 1)
    assert result == [6, 8, 9]

    result = solver.get_list_of_candidates_for_cell(8, 0)
    assert result == [2, 8, 9]

def test_possible_values_for_cell_2(unsolvable_sudoku):
    solver = SudokuSolver(unsolvable_sudoku)

    result = solver.get_list_of_candidates_for_cell(0, 1)
    assert result == []
    
def test_is_solvable_1(unsolvable_sudoku):

    solver = SudokuSolver(unsolvable_sudoku)
    assert not solver.is_solvable()

def test_is_solvable_2(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)
    assert solver.is_solvable()

def test_is_solvable_3(easy_sudoku):
    solver = SudokuSolver(easy_sudoku)
    assert solver.is_solvable()


def test_get_first(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)
    result = solver.get_first_empty()
    assert result == (1, 0, [1, 8, 9])

def test_solve_1(easy_sudoku):
    solver = SudokuSolver(easy_sudoku)
    result = solver.solve()

    assert result is not None

def test_solve_2(hard_sudoku):
    solver = SudokuSolver(hard_sudoku)
    
    result = solver.solve()

    assert result is not None

def test_solve_3():
    grid = [[0] * 9 for _ in range(9)]
    sudoku = Sudoku(grid)
    solver = SudokuSolver(sudoku)

    result = solver.solve()
    
    assert result is None


def test_get_coords(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)

    index = 2
    type = "col"
    result = solver.get_coords_list(index, type)
    expected = [(index, i) for i in range(9)]
    assert result == expected

    type = "row"
    result = solver.get_coords_list(index, type)
    expected = [(i, index) for i in range(9)]
    assert result == expected

    type = "sq"
    result = solver.get_coords_list(index, type)
    expected = [(6, 0), (7, 0), (8, 0),
                (6, 1), (7, 1), (8, 1),
                (6, 2), (7, 2), (8, 2)]
    assert result == expected


def test_indexes_per_candidate(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)
    candidates = [[1, 2],
                  [1, 2, 3],
                  [5, 6],
                  [7, 9],
                  [1, 7],
                  [2, 9],
                  [8, 9],
                  [-1],
                  [1, 3, 6]]
    
    distribution = {
        1: [0, 1, 4, 8],
        2: [0, 1, 5],
        3: [1, 8],
        5: [2],
        6: [2, 8],
        7: [3, 4],
        8: [6],
        9: [3, 5, 6]
    }
    result = solver.get_indexes_per_candidate(candidates)
    assert result == distribution

def test_solve_recursive(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)
    solution = solver.solve_recursive()
    assert solution is None or solution.is_solved()

def test_solve_with_ignore_solution(hard_sudoku):
    solver = SudokuSolver(hard_sudoku)
    first_solution = solver.solve_recursive()
    second_solution = solver.solve_recursive(ignore_solution=first_solution)
    assert second_solution is None or not np.array_equal(first_solution.grid, second_solution.grid)

def test_filter_out_hidden_singles(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)
    solver.grid_of_candidates[0][8] = [3]
    solver.filter_out_hidden_singles([(i, 0) for i in range(9)])
    assert solver.grid_of_candidates[0][8] == [3]

def test_get_highest_candidate_number(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)
    x, y, values = solver.get_highest_candidate_number()
    assert len(values) == max(len(c) for row in solver.grid_of_candidates for c in row if c != [-1])

def test_get_lowest_candidates_number(example_sudoku_1):
    solver = SudokuSolver(example_sudoku_1)
    x, y, values = solver.get_lowest_candidates_number()
    assert len(values) == min(len(c) for row in solver.grid_of_candidates for c in row if c != [-1])
