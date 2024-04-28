from .Sudoku import Sudoku
import numpy as np
from copy import deepcopy
from joblib import load

class SudokuScrambler:
    """
    A class designed to scramble a given Sudoku puzzle to generate a new puzzle configuration
    while potentially maintaining the solution's validity.

    Attributes
    ----------
    sudoku : Sudoku
        The Sudoku instance that is to be scrambled.
    number_of_initial_values : int
        The number of values to remain in the Sudoku grid after scrambling.
    model : any
        A machine learning model loaded to potentially assist with scrambling.
    """
    def __init__(self, sudoku: Sudoku, number_of_initial_values = 0) -> None:
        """
        Initialize a SudokuScrambler with a Sudoku object and optionally the number of initial values.

        Parameters
        ----------
        sudoku : Sudoku
            The Sudoku object to scramble.
        number_of_initial_values : int, optional
            The desired number of non-empty cells in the scrambled Sudoku grid.
        """
        self.sudoku = sudoku
        self.sudoku.initial_grid = np.zeros([9, 9])
        self.number_of_initial_values = number_of_initial_values
        self.model = load("sudoku_model.joblib")

    
    def swap_all_digits(self, digit1: int, digit2: int) -> None:
        """
        Swap two digits everywhere they appear in the Sudoku grid.

        Parameters
        ----------
        digit1 : int
            The first digit to swap.
        digit2 : int
            The second digit to swap.
        """
        self.sudoku.grid[self.sudoku.grid == digit1] = -1
        self.sudoku.grid[self.sudoku.grid == digit2] = digit1
        self.sudoku.grid[self.sudoku.grid == -1 ] = digit2 
        
    def permutate_rows(self, new_order: list) -> None:
        """
        Permutate the rows of the Sudoku grid according to a new order.

        Parameters
        ----------
        new_order : list
            The new order of row indices.
        """
        self.sudoku.grid = self.sudoku.grid[new_order, :]

    def permutate_cols(self, new_order: list) -> None:
        """
        Permutate the columns of the Sudoku grid according to a new order.

        Parameters
        ----------
        new_order : list
            The new order of column indices.
        """
        self.sudoku.grid = self.sudoku.grid[:, new_order]

    @staticmethod
    def shuffle_order_within_squares() -> list:
        """
        Generate a new order for rows or columns within each 3x3 square.

        Returns
        -------
        list
            The new order indices for the rows or columns within the squares.
        """
        new_order = []
        for i in range(0, 9, 3):
            sub_order = np.arange(0, 3)
            sub_order = np.random.permutation(sub_order)
            sub_order += i
            new_order += list(sub_order)

        return new_order

    @staticmethod
    def shuffle_order_with_blocks() -> list:
        """
        Shuffle the order of 3x3 blocks in the Sudoku grid.

        Returns
        -------
        list
            The new order indices for the blocks.
        """
        new_order = []
        sub_order = np.arange(0, 3)
        sub_order = np.random.permutation(sub_order)
        for i in sub_order:
            sub_arr = np.arange(0, 3)
            new_order += list(sub_arr + i * 3)
        
        return new_order

    def rotate_grid(self) -> None:
        """
        Rotate the entire Sudoku grid by 90 degrees counterclockwise.
        """
        self.sudoku.grid = np.rot90(self.sudoku.grid)
    
    def reflect_grid(self, axis: int) -> None:
        """
        Reflect the Sudoku grid across a specified axis.

        Parameters
        ----------
        axis : int
            The axis to reflect across (0 for horizontal, 1 for vertical).
        """
        if axis == 0:
            self.sudoku.grid = np.fliplr(self.sudoku.grid)
        if axis == 1:
            self.sudoku.grid = np.flipud(self.sudoku.grid)

    def remove_digit(self, index: int) -> None:
        """
        Remove a digit from a specified position in the grid.

        Parameters
        ----------
        index : int
            The index in the flat grid where the digit will be removed.
        """
        x = index % 9
        y = index // 9
        self.sudoku.clean_cell(x, y)

    def update_initial_grid(self) -> None:
        """
        Update the initial grid state to the current grid state after all modifications.
        """
        self.sudoku.initial_grid = deepcopy(self.sudoku.grid)


    def scramble(self) -> None:
        """
        Perform a series of operations to scramble the Sudoku grid. This includes swapping digits,
        permutating rows and columns, rotating, and removing digits to prepare a new puzzle.
        """
        # swapping digits
        random_digits1 = np.random.randint(1, 10, size=10)
        random_digits2 = np.random.randint(1, 10, size=10)
        pairs_to_swap = zip(random_digits1, random_digits2)    
        for d1, d2 in pairs_to_swap:
            self.swap_all_digits(d1, d2)

        # shuffling rows
        new_order = self.shuffle_order_within_squares()
        self.permutate_rows(new_order)

        # shuffling cols
        new_order = self.shuffle_order_within_squares()
        self.permutate_cols(new_order)

        # shuffling blocks
        new_order = self.shuffle_order_with_blocks()
        self.permutate_rows(new_order)
        new_order = self.shuffle_order_with_blocks()
        self.permutate_cols(new_order)

        # rotating
        random_rotation = np.random.randint(0, 4)
        for _ in range(random_rotation):
            self.rotate_grid()
            
        # removing digits
        numbers_to_be_removed = np.arange(82)
        if self.number_of_initial_values != 0:
            lenght = 81 - self.number_of_initial_values
        else:
            lenght = np.random.randint(0, 65)
        digits_to_be_removed = np.random.choice(numbers_to_be_removed, size=lenght, replace=False)
        for d in digits_to_be_removed:
            self.remove_digit(d)
        
        # saving puzzle
        self.update_initial_grid()

                