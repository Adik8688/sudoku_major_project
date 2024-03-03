from .Sudoku import Sudoku
import numpy as np
from copy import deepcopy

class SudokuScrambler:
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        self.sudoku.initial_grid = np.zeros([9, 9])

    
    def swap_all_digits(self, digit1: int, digit2: int) -> None:
        self.sudoku.grid[self.sudoku.grid == digit1] = -1
        self.sudoku.grid[self.sudoku.grid == digit2] = digit1
        self.sudoku.grid[self.sudoku.grid == -1 ] = digit2 
        
    def shuffle_rows(self, new_order: list) -> None:
        self.sudoku.grid = self.sudoku.grid[new_order, :]

    def shuffle_cols(self, new_order: list) -> None:
        self.sudoku.grid = self.sudoku.grid[:, new_order]


    def rotate_grid(self) -> None:
        self.sudoku.grid = np.rot90(self.sudoku.grid)
    
    def reflect_grid(self, axis: int) -> None:
        if axis == 0:
            self.sudoku.grid = np.fliplr(self.sudoku.grid)
        if axis == 1:
            self.sudoku.grid = np.flipud(self.sudoku.grid)

    def remove_digit(self, index) -> None:
        x = index % 9
        y = index // 9
        self.sudoku.clean_cell(x, y)

    def update_initial_grid(self) -> None:
        self.sudoku.initial_grid = deepcopy(self.sudoku.grid)

    def scramble(self) -> None:
        # swapping digits
        random_digits1 = np.random.randint(1, 10, size=10)
        random_digits2 = np.random.randint(1, 10, size=10)
        pairs_to_swap = zip(random_digits1, random_digits2)    
        for d1, d2 in pairs_to_swap:
            self.swap_all_digits(d1, d2)

        # shuffling rows
        new_order = np.arange(0, 9)
        new_order = np.random.permutation(new_order)
        self.shuffle_rows(new_order)

        # shuffling cols
        new_order = np.random.permutation(new_order)
        self.shuffle_cols(new_order)

        # rotating
        random_rotation = np.random.randint(0, 4)
        for _ in range(random_rotation):
            self.rotate_grid()
        
        # TO DO
        # random_reflection = np.random.randint()
            
        # removing digits
        all_indexes = np.arange(0, 82)
        shuffled_indexes = np.random.permutation(all_indexes)
        number_of_digits_to_be_removed = np.random.randint(0, 82)
        digits_to_be_removed = shuffled_indexes[:number_of_digits_to_be_removed]
        for d in digits_to_be_removed:
            self.remove_digit(d)
        
        # saving puzzle
        self.update_initial_grid()

                