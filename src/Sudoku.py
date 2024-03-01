import copy
import numpy as np


class Sudoku:
    def __init__(self, grid: list) -> None:
        if isinstance(grid, str):
            grid = self.string_to_grid(grid)

        self.initial_grid = copy.deepcopy(np.array(grid))
        self.grid = np.array(grid)
        self.grid_validation()

    def grid_validation(self) -> None:
        if self.grid.shape != (9, 9):
            exit(1)

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
            return self.grid[y][x]
        return -1

    def set_cell(self, x: int, y: int, new_value: int) -> None:
        if (
            self.valid_coords(x, y)
            and self.valid_value(new_value)
            and self.initial_grid[y][x] == 0
        ):
            self.grid[y][x] = new_value

    def check_rows(self) -> bool:
        for row in self.grid:
            if sorted(row) != list(range(1, 10)):
                return False
        return True

    def check_cols(self) -> bool:
        for col in range(9):
            col_values = [self.grid[col][row] for row in range(9)]
            if sorted(col_values) != list(range(1, 10)):
                return False

        return True

    def check_squares(self) -> bool:
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                square_values = []
                for x in range(3):
                    for y in range(3):
                        square_values.append(self.grid[j + y][i + x])
                if sorted(square_values) != list(range(1, 10)):
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

    def __str__(self) -> str:
        output = ""
        for row in self.grid:
            output += " ".join([(str(i) if i != 0 else "-") for i in row])
            output += "\n"

        return output
