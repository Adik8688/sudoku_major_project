from .Sudoku import Sudoku
from collections import defaultdict
from copy import deepcopy
import numpy as np

class SudokuSolver:
    """
    A class designed to solve Sudoku puzzles using various advanced techniques including
    backtracking and the application of hidden singles and other advanced strategies.

    Attributes
    ----------
    sudoku : Sudoku
        The Sudoku puzzle to solve.
    output_file : str
        Path to the output file where the solver's steps are logged.
    """
    def __init__(self, sudoku: Sudoku, output_file="output_solver.txt") -> None:
        """
        Initialize a SudokuSolver with a Sudoku instance and an optional output file.

        Parameters
        ----------
        sudoku : Sudoku
            The Sudoku puzzle to solve.
        output_file : str
            The file path to record solving steps.
        """
        self.sudoku = sudoku
        self.create_grid_of_candidates()
        self.number_of_steps = 0
        self.output_file = output_file
        

    def get_list_of_candidates_for_cell(self, x: int, y: int) -> list:
        """
        Retrieve a list of possible values for a specific cell, based on Sudoku rules.

        Parameters
        ----------
        x : int
            The column index of the cell.
        y : int
            The row index of the cell.

        Returns
        -------
        list
            A list of valid values that can be placed in the cell; returns [-1] if the cell is filled.
        """
        if self.sudoku.get_cell(x, y) != 0:
            return [-1]
        
        invalid_values = []
        invalid_values += self.sudoku.get_row(y).tolist()
        invalid_values += self.sudoku.get_col(x).tolist()
        sq_index = x // 3 + 3 * (y // 3)
        invalid_values += self.sudoku.get_square(sq_index).flatten().tolist()
        
        valid_values = [i for i in range(1, 10) if i not in invalid_values]

        return valid_values


    def create_grid_of_candidates(self):
        """
        Create a grid mapping each cell to its list of possible candidates.
        """
        self.grid_of_candidates = []
        for y in range(9):
            row = []
            for x in range(9):
                row.append(self.get_list_of_candidates_for_cell(x, y))
            self.grid_of_candidates.append(row)
    
    def is_solvable(self) -> bool:
        """
        Check if the current state of the Sudoku puzzle is solvable based on candidate lists.

        Returns
        -------
        bool
            True if the puzzle is potentially solvable, False if any cell has no candidates.
        """
        for row in self.grid_of_candidates:
            for i in row:
                if not i:
                    return False
        return True
    
    def get_first_empty(self) -> tuple:
        """
        Find the first empty cell in the Sudoku grid and return its coordinates along with its valid candidates.

        Returns
        -------
        tuple
            A tuple (x, y, values) where x and y are coordinates of the cell, and values are the possible candidates.
            Returns (-1, -1, []) if no empty cell is found.
        """
        for y in range(9):
            for x in range(9):
                if self.sudoku.get_cell(x, y) == 0:
                    values = self.get_list_of_candidates_for_cell(x, y)
                    return (x, y, values)
        return (-1, -1, [])
    
    def get_lowest_candidates_number(self) -> tuple:
        """
        Find the cell with the smallest number of candidate values and return its coordinates and candidates.

        Returns
        -------
        tuple
            A tuple (x, y, values) where x and y are the coordinates of the cell and values are its candidate numbers.
        """
        x, y, values = -1, -1, list(range(10))
        for i in range(9):
            for j in range(9):
                if len(self.grid_of_candidates[i][j]) < len(values) and self.grid_of_candidates[i][j] != [-1]:
                    x, y, values = j, i, self.grid_of_candidates[i][j]
        
        return x, y, values
    
    def get_highest_candidate_number(self) -> tuple:
        """
        Find the cell with the highest number of candidate values and return its coordinates and candidates.

        Returns
        -------
        tuple
            A tuple (x, y, values) where x and y are the coordinates of the cell and values are its candidate numbers.
        """
        x, y, values = -1, -1, []
        for i in range(9):
            for j in range(9):
                if len(self.grid_of_candidates[i][j]) > len(values) and self.grid_of_candidates[i][j] != [-1]:
                    x, y, values = j, i, self.grid_of_candidates[i][j]
        
        return x, y, values
    
    @staticmethod
    def get_indexes_per_candidates(list_of_candidates: list) -> dict:
        """
        Group cell indices by candidate numbers to help identify unique candidates.

        Parameters
        ----------
        list_of_candidates : list
            A list of candidate lists for a subset of cells.

        Returns
        -------
        dict
            A dictionary mapping each candidate number to the list of indices where it appears.
        """
        distribution = defaultdict(list)

        for i, candidates in enumerate(list_of_candidates):
            if candidates != [-1]:
                for c in candidates:
                    distribution[c].append(i)
        
        return dict(sorted(distribution.items()))
    
    def filter_out_hidden_singles(self, coords: list):
        """
        Filter out hidden singles within a specific subset of cells.

        Parameters
        ----------
        coords : list
            A list of coordinates specifying the subset of cells to check.
        """
        candidates = [self.grid_of_candidates[y][x] for x, y in coords]
        distribution = self.get_indexes_per_candidates(candidates)

        for k, v in distribution.items():
            if len(v) == 1:
                x, y = coords[v[0]]
                self.grid_of_candidates[y][x] = [k]
    
    @staticmethod
    def get_coords_list(index: int, type: str) -> list:
        """
        Get a list of coordinates corresponding to a row, column, or square.

        Parameters
        ----------
        index : int
            The index of the row, column, or square.
        type : str
            Specifies whether the coordinates are for a 'row', 'col', or 'sq' (square).

        Returns
        -------
        list
            A list of coordinates for the specified row, column, or square.
        """
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
        """
        Apply advanced solving techniques to reduce the candidates grid and possibly identify certain values.
        """
        while True:
            old_grid = deepcopy(self.grid_of_candidates)
            for index in range(9):
                for type in ["col", "row", "sq"]:
                    coords = self.get_coords_list(index, type)
                    self.filter_out_hidden_singles(coords)
            
            if self.grid_of_candidates == old_grid:
                break
    
    def solve(self) -> Sudoku:
        """
        Solve the Sudoku puzzle by recursively applying solving techniques and backtracking if necessary.

        Returns
        -------
        Sudoku
            The solved Sudoku instance, or None if no solution is found.
        """
        with open(self.output_file, 'w') as f:
            f.write(f"")
        
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
        """
        Recursively solve the Sudoku puzzle by trying each candidate in the cell with the fewest candidates
        and backtrack if a dead end is reached.

        Parameters
        ----------
        n : int, optional
            The depth of the recursive call, used primarily for debugging and logging.
        ignore_solution : Sudoku, optional
            An optional Sudoku instance to ignore as a solution, used in finding multiple solutions.

        Returns
        -------
        Sudoku
            The Sudoku instance if solved; None if no solution is found or if the ignore_solution is met.
        """
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
            if ignore_solution is None:
                with open(self.output_file, 'a') as f:
                    f.write(f"{x} {y} {value} {n}\n")
            self.sudoku.set_cell(x, y, value)
            self.create_grid_of_candidates()
            result = self.solve_recursive(n = n + 1, ignore_solution=ignore_solution)
            if result is not None:
                return self.sudoku
            
        if ignore_solution is None:
            with open(self.output_file, 'a') as f:
                f.write(f"{x} {y} 0 {n}\n")
        self.sudoku.clean_cell(x, y)
        self.create_grid_of_candidates()


        return None
    
  