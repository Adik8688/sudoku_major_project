from src.Sudoku import Sudoku
import numpy as np
from collections import defaultdict


class SudokuAnalyzer:
    """
    A class to analyze various properties of a Sudoku puzzle.

    Attributes
    ----------
    sudoku : Sudoku
        An instance of the Sudoku class to be analyzed.
    """
    def __init__(self, sudoku: Sudoku) -> None:
        """
        Initialize the SudokuAnalyzer with a Sudoku object.

        Parameters
        ----------
        sudoku : Sudoku
            The Sudoku object to analyze.
        """
        self.sudoku = sudoku

    def get_sum_of_candidates(self) -> int:
        """
        Calculate the total number of valid candidate numbers for all empty cells in the Sudoku grid.

        Returns
        -------
        int
            The sum of all candidates that can be filled into the empty cells.
        """
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
        """
        Count the number of cells in the Sudoku grid that are not empty.

        Returns
        -------
        int
            The number of cells that are filled with a number other than zero.
        """
        return np.count_nonzero(self.sudoku.grid)

    def get_distribution_of_initial_numbers(self) -> dict:
        """
        Compute the distribution of the numbers initially present in the Sudoku grid.

        Returns
        -------
        dict
            A dictionary where keys are the numbers and values are the frequency of each number in the grid.
        """
        non_zeros = self.sudoku.grid[self.sudoku.grid != 0]
        distribution = defaultdict(int)

        for i in non_zeros:
            distribution[i] += 1

        return distribution

    def convert_distribution_to_entropy(self, distribution: dict) -> int:
        """
        Calculate the entropy of the distribution of initial numbers in the Sudoku grid.

        Parameters
        ----------
        distribution : dict
            A dictionary containing the frequency of each number.

        Returns
        -------
        float
            The entropy of the distribution, rounded to two decimal places.
        """
        total = sum(distribution.values())

        entropy = 0
        for v in distribution.values():
            entropy -= (v/total) * np.log2(v/total)

        return round(entropy, 2)
    
    def get_sudoku_description(self) -> tuple:
        """
        Generate a comprehensive description of the Sudoku's current state.

        Returns
        -------
        tuple
            A tuple containing the sum of candidates, number of initial values, and the entropy of initial values.
        """
        sum_of_candidates = self.get_sum_of_candidates()
        number_of_initial_values = self.get_number_of_non_empty_cells()

        initial_numbers_distribution = self.get_distribution_of_initial_numbers()
        initial_numbers_entropy = self.convert_distribution_to_entropy(initial_numbers_distribution)

        return (sum_of_candidates, number_of_initial_values, initial_numbers_entropy)
    
    def __str__(self) -> str:
        """
        Provide a string representation of the Sudoku analysis.

        Returns
        -------
        str
            A formatted string showing the analysis results.
        """
        properties = self.get_sudoku_description()
        
        return f"Sum of candidates: {properties[0]}\nNumber of initial values: {properties[1]}\nInitial values' entropy: {properties[2]}"
    