from .Sudoku import Sudoku

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
                invalid_values.append(self.sudoku.get_cell(i + sqx * 3, j + sqy * 3))
        
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
    
    def is_solvable(self) -> bool:
        grid_of_possibilities = self.get_grid_of_possibilities()
        for row in grid_of_possibilities:
            for i in row:
                if not i:
                    return False
        return True
    
    def get_first_empty(self) -> tuple:
        for y in range(9):
            for x in range(9):
                if self.sudoku.get_cell(x, y) == 0:
                    return (x, y)
        return (-1, -1)
    
    def solve(self, n = 0) -> Sudoku:
        if self.sudoku.is_solved():
            return self.sudoku

        if not self.is_solvable():
            return None
        
        x, y = self.get_first_empty()
        values = self.get_list_of_possibilities_for_cell(x, y)

        for value in values:
            self.sudoku.set_cell(x, y, value)
            print(x, y, value, n)
            result = self.solve(n + 1)
            if result is not None:
                return self.sudoku
        
        self.sudoku.set_cell(x, y, 0)

        return None
    
  