import copy


class Sudoku:
    def __init__(self, grid: list) -> None:
        if isinstance(grid, str):
            grid = self.string_to_grid(grid)

        if not self.valid_grid_size(grid):
            exit(1)

        self.initial_grid = copy.deepcopy(grid)
        self.grid = grid


    @staticmethod
    def valid_grid_size(grid: list) -> bool:
        if len(grid) != 9:
            return False
        
        for row in grid:
            if len(row) != 9:
                return False
        
        return True


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
    
    def __str__(self) -> str:
        for row in self.grid:
            print(" ".join([(str(i) if i != 0 else "-") for i in row]))