import os

class SudokuDB:
    def __init__(self) -> None:
        self.filepath = 'sudoku_db.csv'

    
    def get_sudoku_by_diff(self, desired_difficulty):
        delta = 10
        choice = None
        with open(self.filepath) as f:
            f.readline()
            for line in f:
                diff = float(line.split(";")[-1].strip())
                if abs(diff - desired_difficulty) > delta:
                    return choice
                
                delta = abs(diff - desired_difficulty)
                choice = line
        
        if choice is not None:
            return choice.split(";")[0]
        return choice