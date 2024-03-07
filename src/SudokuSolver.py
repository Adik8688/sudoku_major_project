from .Sudoku import Sudoku
from collections import defaultdict
from copy import deepcopy
import numpy as np

class SudokuSolver:
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        self.grid_of_candidates = []
        self.create_grid_of_candidates()
        self.number_of_steps = 0

    def get_list_of_candidates_for_cell(self, x: int, y: int) -> list:
        if self.sudoku.get_cell(x, y) != 0:
            return [-1]
        
        invalid_values = []
        invalid_values += self.sudoku.get_row(y).tolist()
        invalid_values += self.sudoku.get_col(x).tolist()
        sq_index = x // 3 + 3 * (y // 3)
        invalid_values += self.sudoku.get_square(sq_index).flatten().tolist()
        
        valid_values = [i for i in range(1, 10) if i not in invalid_values]

        return valid_values


    def create_grid_of_candidates(self) -> list:
        for y in range(9):
            row = []
            for x in range(9):
                row.append(self.get_list_of_candidates_for_cell(x, y))
            self.grid_of_candidates.append(row)

    def update_grid_of_candidates(self, x: int, y: int) -> list:
        # cols and rows
        for i in range(9):
            self.grid_of_candidates[y][i] = self.get_list_of_candidates_for_cell(i, y)
            self.grid_of_candidates[i][x] = self.get_list_of_candidates_for_cell(x, i)

        # squares
        sqx = x // 3
        sqy = y // 3
        for i in range(3):
            for j in range(3):
                x_coord = sqx * 3 + i
                y_coord = sqy * 3 + j
                self.grid_of_candidates[y_coord][x_coord] = self.get_list_of_candidates_for_cell(x_coord, y_coord)
        
    
    def is_solvable(self) -> bool:
        for row in self.grid_of_candidates:
            for i in row:
                if not i:
                    return False
        return True
    
    def get_first_empty(self) -> tuple:
        for y in range(9):
            for x in range(9):
                if self.sudoku.get_cell(x, y) == 0:
                    values = self.get_list_of_candidates_for_cell(x, y)
                    return (x, y, values)
        return (-1, -1, [])
    
    def get_lowest_candidates_number(self) -> tuple:
        x, y, values = -1, -1, list(range(10))
        for i in range(9):
            for j in range(9):
                if len(self.grid_of_candidates[i][j]) < len(values) and self.grid_of_candidates[i][j] != [-1]:
                    x, y, values = j, i, self.grid_of_candidates[i][j]
        
        return x, y, values
    
    def get_highest_candidate_number(self) -> tuple:
        x, y, values = -1, -1, []
        for i in range(9):
            for j in range(9):
                if len(self.grid_of_candidates[i][j]) > len(values) and self.grid_of_candidates[i][j] != [-1]:
                    x, y, values = j, i, self.grid_of_candidates[i][j]
        
        return x, y, values
    
    @staticmethod
    def get_indexes_per_candidate(list_of_candidates: list) -> dict:
        distribution = defaultdict(list)

        for i, candidates in enumerate(list_of_candidates):
            if candidates != [-1]:
                for c in candidates:
                    distribution[c].append(i)
        
        return dict(sorted(distribution.items()))
    
    def filter_out_hidden_singles(self, coords: list):
        candidates = [self.grid_of_candidates[y][x] for x, y in coords]
        distribution = self.get_indexes_per_candidate(candidates)

        for k, v in distribution.items():
            if len(v) == 1:
                x, y = coords[v[0]]
                self.grid_of_candidates[y][x] = [k]
    
    @staticmethod
    def get_coords_list(index: int, type: str) -> list:
        if not 0 <= index < 9:
            return []

        if type == "col":
            x_coords = [index] * 9
            y_coords = list(range(9))
            return list(zip(x_coords, y_coords))
        
        if type == "row":
            x_coords = list(range(9))
            y_coords = [index] * 9
            return list(zip(x_coords, y_coords))
        
        sqx = index % 3
        sqy = index // 3
        coords = []
        for y in range(3):
            for x in range(3):
                coords.append((x + sqx * 3, y + sqy * 3))

        return coords
    
    def apply_advance_rules(self) -> None:
        while True:
            old_grid = deepcopy(self.grid_of_candidates)
            for index in range(9):
                for type in ["col", "row", "sq"]:
                    coords = self.get_coords_list(index, type)
                    self.filter_out_hidden_singles(coords)
            
            if self.grid_of_candidates == old_grid:
                break
    
    def solve(self) -> Sudoku:
        solution = self.solve_recursive()
        if solution is None:
            return None
        solution = deepcopy(solution)
        self.sudoku.reset_sudoku()
        self.grid_of_candidates = []
        self.create_grid_of_candidates()

        steps = deepcopy(self.number_of_steps)

        another_solution = self.solve_recursive(ignore_solution=solution)
        if another_solution is not None:
            return None
        
        self.number_of_steps = steps

        return solution


    
    def solve_recursive(self, n: int = 0, ignore_solution: Sudoku = None) -> Sudoku:
        self.number_of_steps += 1
        if ignore_solution is not None and np.array_equal(self.sudoku.grid, ignore_solution.grid):
            return None
        
        if not self.is_solvable():
            return None
        
        if self.sudoku.is_solved():
            return self.sudoku
        
        self.apply_advance_rules()
        x, y, values = self.get_lowest_candidates_number()

        for value in values:
            self.sudoku.set_cell(x, y, value)
            self.update_grid_of_candidates(x, y)
            result = self.solve_recursive(n = n + 1, ignore_solution=ignore_solution)
            if result is not None:
                return self.sudoku
        
        self.sudoku.clean_cell(x, y)
        self.update_grid_of_candidates(x, y)

        return None
    
  