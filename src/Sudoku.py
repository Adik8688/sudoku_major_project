import copy
import numpy as np


class Sudoku:
    def __init__(self, grid: list) -> None:
        if isinstance(grid, str):
            grid = self.string_to_grid(grid)

        self.initial_grid = copy.deepcopy(np.array(grid))
        self.grid = np.array(grid, dtype=int)
        self.grid_validation()

    def grid_validation(self) -> None:
        if self.grid.shape != (9, 9):
            exit(1)

    def reset_sudoku(self) -> None:
        self.grid = copy.deepcopy(self.initial_grid)

    @staticmethod
    def string_to_grid(grid: str) -> list:
        output = []
        for row in grid.strip().split():
            new_row = [int(i) for i in list(row)]
            output.append(new_row)
        return output

    @staticmethod
    def valid_coords(x: int, y: int) -> bool:
        return 0 <= x < 9 and 0 <= y < 9

    @staticmethod
    def valid_value(value: int) -> bool:
        return 0 <= value <= 9

    def get_cell(self, x: int, y: int) -> int:
        if self.valid_coords(x, y):
            return self.grid[y, x]
        return -1

    def set_cell(self, x: int, y: int, new_value: int) -> None:
        if (
            self.valid_coords(x, y)
            and self.valid_value(new_value)
            and self.initial_grid[y, x] == 0 
        ):
            self.grid[y, x] = new_value

    def clean_cell(self, x: int, y: int) -> None:
        self.set_cell(x, y, 0)

    def check_rows(self) -> bool:
        row_correct = np.all(np.sort(self.grid, axis=1) == np.arange(1, 10), axis=1)
        return np.all(row_correct)

    def check_cols(self) -> bool:
        col_correct = np.all(np.sort(self.grid, axis = 0) == np.arange(1, 10)[:, None], axis=0)
        return np.all(col_correct)

    def check_squares(self) -> bool:
        for i in range(9):
            square = self.get_square(i)
            if not np.all(np.sort(square.flatten()) == np.arange(1, 10)):
                return False
        return True

    def is_solved(self) -> bool:
        return self.check_rows() and self.check_cols() and self.check_squares()

    def get_col(self, index: int) -> np.array:
        return self.grid[:, index]

    def get_row(self, index: int) -> np.array:
        return self.grid[index, :]

    def get_square(self, index: int) -> np.array:
        x = (index % 3) * 3
        y = (index // 3) * 3
        return self.grid[y : y + 3, x : x + 3]

    def get_hash(self) -> str:
        output = ""
        for row in self.grid:
            for i in row:
                output += str(i)
        
        return output

    def __str__(self) -> str:
        output = ""
        for y in range(9):
            for x in range(9):
                if self.grid[y, x] != 0:
                    output += f"{self.grid[y, x]} "
                else:
                    output += "- "
            output += "\n"

        return output
    
    def str_with_colors(self) -> str:
        COLOR = '\033[91m'
        ENDC = '\033[0m'
        output = ""
        for y in range(9):
            for x in range(9):
                if self.grid[y, x] != 0 and self.grid[y, x] == self.initial_grid[y, x]:
                    output += f"{COLOR}{self.grid[y, x]}{ENDC} "
                else:
                    output += f"{self.grid[y, x]} "
            output += "\n"

        return output
