from src.Sudoku import Sudoku

class SudokuAnalyzer:
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku

    def get_sum_of_candidates(self) -> int:
        result = 0
        for y in range(9):
            for x in range(9):
                if self.sudoku.get_cell(x, y) == 0:
                    possible_values = set(range(1, 10)) - (
                        set(self.sudoku.get_row(y)) |
                        set(self.sudoku.get_col(x)) |
                        set(self.sudoku.get_square(x // 3 + 3 * (y // 3)).flatten())
                    )
                    result += len(possible_values)
        
        return result

