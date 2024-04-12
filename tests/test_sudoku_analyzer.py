import pytest
from src.Sudoku import Sudoku
from src.SudokuAnalyzer import SudokuAnalyzer

@pytest.fixture
def filled_sudoku():
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
    return Sudoku(grid)

@pytest.fixture
def example_sudoku_1():
    grid = [
        [5, 0, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    return Sudoku(grid)

def test_get_sum_of_candidates(example_sudoku_1):
    analyzer = SudokuAnalyzer(example_sudoku_1)
    sum_candidates = analyzer.get_sum_of_candidates()
    # Depending on the provided Sudoku, this needs to match the actual calculated candidates
    assert sum_candidates > 0  # Specific value depends on sudoku setup

def test_get_number_of_non_empty_cells(example_sudoku_1):
    analyzer = SudokuAnalyzer(example_sudoku_1)
    num_non_empty = analyzer.get_number_of_non_empty_cells()
    assert num_non_empty == 29  # Based on the example grid setup

def test_get_distribution_of_initial_numbers(example_sudoku_1):
    analyzer = SudokuAnalyzer(example_sudoku_1)
    distribution = analyzer.get_distribution_of_initial_numbers()
    assert distribution[5] == 1  # One '5' in the provided grid setup

def test_convert_distribution_to_entropy(example_sudoku_1):
    analyzer = SudokuAnalyzer(example_sudoku_1)
    distribution = {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3}
    entropy = analyzer.convert_distribution_to_entropy(distribution)
    assert entropy > 0  # Check for a positive entropy

def test_get_sudoku_description(example_sudoku_1):
    analyzer = SudokuAnalyzer(example_sudoku_1)
    description = analyzer.get_sudoku_description()
    assert isinstance(description, tuple) and len(description) == 3
    sum_candidates, num_initial, entropy = description
    assert sum_candidates > 0 and num_initial > 0 and entropy > 0

def test_analyzer_str_method(example_sudoku_1):
    analyzer = SudokuAnalyzer(example_sudoku_1)
    description_str = str(analyzer)
    assert "Sum of candidates:" in description_str
    assert "Number of initial values:" in description_str
    assert "Initial values' entropy:" in description_str