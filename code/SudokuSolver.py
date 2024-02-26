from code.Sudoku import Sudoku

class SudokuSolver:
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku

    def get_list_of_possibilities_for_cell(self, x: int, y: int) -> list:
        if self.sudoku.get_cell(x, y) != 0:
            return [-1]
        
        invalid_values = []
        for i in range(9):
            invalid_values.append(self.sudoku.get_cell(x, i))
            invalid_values.append(self.sudoku.get_cell(i, y))
        
        sqx = x // 3
        sqy = y // 3
        for i in range(3):
            for j in range(3):
                invalid_values.append(self.sudoku.get_cell(i + sqx, j + sqy))
        
        valid_values = [i for i in range(1, 10) if i not in invalid_values]

        return valid_values


    def get_grid_of_possibilities(self) -> list:
        grid = []
        for y in range(9):
            row = []
            for x in range(9):
                row.append(self.get_list_of_possibilities_for_cell(x, y))
            grid.append(row)

        return grid