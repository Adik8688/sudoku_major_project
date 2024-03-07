from src.Sudoku import Sudoku
import numpy as np
from collections import defaultdict


class SudokuAnalyzer:
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku

    def get_sum_of_candidates(self) -> int:
        result = 0
        for y in range(9):
            for x in range(9):
                if self.sudoku.get_cell(x, y) == 0:
                    possible_values = set(range(1, 10)) - (
                        set(self.sudoku.get_row(y))
                        | set(self.sudoku.get_col(x))
                        | set(self.sudoku.get_square(x // 3 + 3 * (y // 3)).flatten())
                    )
                    result += len(possible_values)

        return result

    def get_number_of_non_empty_cells(self) -> int:
        return np.count_nonzero(self.sudoku.grid)

    def get_distribution_of_initial_numbers(self) -> dict:
        non_zeros = self.sudoku.grid[self.sudoku.grid != 0]
        distribution = defaultdict(int)

        for i in non_zeros:
            distribution[i] += 1

        return distribution

    @staticmethod
    def convert_distribution_to_entropy(distribution: dict) -> int:
        total = sum(distribution.values())

        entropy = 0
        for v in distribution.values():
            entropy -= (v/total) * np.log2(v/total)

        return round(entropy, 2)
    
    def get_sudoku_description(self) -> tuple:
        sum_of_candidates = self.get_sum_of_candidates()
        number_of_initial_values = self.get_number_of_non_empty_cells()

        initial_numbers_distribution = self.get_distribution_of_initial_numbers()
        initial_numbers_entropy = self.convert_distribution_to_entropy(initial_numbers_distribution)

        return (sum_of_candidates, number_of_initial_values, initial_numbers_entropy)
    