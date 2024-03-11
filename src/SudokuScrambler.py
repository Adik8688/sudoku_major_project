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
        
    def permutate_rows(self, new_order: list) -> None:
        self.sudoku.grid = self.sudoku.grid[new_order, :]

    def permutate_cols(self, new_order: list) -> None:
        self.sudoku.grid = self.sudoku.grid[:, new_order]

    @staticmethod
    def shuffle_order_within_squares() -> list:
        new_order = []
        for i in range(0, 9, 3):
            sub_order = np.arange(0, 3)
            sub_order = np.random.permutation(sub_order)
            sub_order += i
            new_order += list(sub_order)

        return new_order

    @staticmethod
    def shuffle_order_with_blocks() -> list:
        new_order = []
        sub_order = np.arange(0, 3)
        sub_order = np.random.permutation(sub_order)
        for i in sub_order:
            sub_arr = np.arange(0, 3)
            new_order += list(sub_arr + i * 3)
        
        return new_order

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
        
        # TO DO
        # random_reflection = np.random.randint()
            
        # removing digits
        numbers_to_be_removed = np.arange(82)
        lenght = np.random.randint(0, 65)
        digits_to_be_removed = np.random.choice(numbers_to_be_removed, size=lenght, replace=False)
        for d in digits_to_be_removed:
            self.remove_digit(d)
        
        # saving puzzle
        self.update_initial_grid()

                