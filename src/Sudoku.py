import copy
import numpy as np


class Sudoku:
    """
    Class for representing and manipulating a Sudoku game.

    Attributes
    ----------
    initial_grid : np.array
        The initial state of the Sudoku grid, stored as a NumPy array.
    grid : np.array
        The current state of the Sudoku grid, stored as a NumPy array.
    """
    def __init__(self, grid: list = ("0" * 9 + "\n") * 9) -> None:
        """
        Initialize a new Sudoku game instance.

        Parameters
        ----------
        grid : list or str
            The initial grid for the Sudoku, either as a list of integers or a string.
        """
        if isinstance(grid, str):
            grid = self.string_to_grid(grid)

        self.initial_grid = copy.deepcopy(np.array(grid))
        self.grid = np.array(grid, dtype=int)
        self.grid_validation()


    def grid_validation(self) -> None:
        """
        Validate the shape of the grid to ensure it is a 9x9 matrix.
        """
        if self.grid.shape != (9, 9):
            exit(1)

    def reset_sudoku(self) -> None:
        """
        Reset the Sudoku to its initial state.
        """
        self.grid = copy.deepcopy(self.initial_grid)


    @staticmethod
    def string_to_grid(grid: str) -> list:
        """
        Convert a string representation of a Sudoku grid into a list format.

        Parameters
        ----------
        grid : str
            String representation of the Sudoku grid.

        Returns
        -------
        list
            The grid converted to a list of lists of integers.
        """
        output = []

        if len(grid.strip().split()) != 9:
            grid_fixed = ""
            for i in range(0, 81, 9):
                grid_fixed += grid[i : i + 9] + "\n"
            grid = grid_fixed

        for row in grid.strip().split():
            new_row = [int(i) for i in list(row)]
            output.append(new_row)
        return output

    @staticmethod
    def valid_coords(x: int, y: int) -> bool:
        """
        Check if the provided coordinates are within the valid range for a Sudoku grid.

        Parameters
        ----------
        x : int
            Column index.
        y : int
            Row index.

        Returns
        -------
        bool
            True if coordinates are valid, False otherwise.
        """
        return 0 <= x < 9 and 0 <= y < 9

    @staticmethod
    def valid_value(value: int) -> bool:
        """
        Check if the provided value is a valid Sudoku value (0 through 9).

        Parameters
        ----------
        value : int
            The value to check.

        Returns
        -------
        bool
            True if the value is valid, False otherwise.
        """
        return 0 <= value <= 9

    def get_cell(self, x: int, y: int) -> int:
        """
        Retrieve the value from a specific cell in the Sudoku grid.

        Parameters
        ----------
        x : int
            Column index.
        y : int
            Row index.

        Returns
        -------
        int
            The value of the cell or -1 if coordinates are invalid.
        """
        if self.valid_coords(x, y):
            return self.grid[y, x]
        return -1

    def set_cell(self, x: int, y: int, new_value: int) -> None:
        """
        Set a new value for a specific cell in the Sudoku grid, if the coordinates and value are valid.

        Parameters
        ----------
        x : int
            Column index.
        y : int
            Row index.
        new_value : int
            The new value to set.
        """
        if (
            self.valid_coords(x, y)
            and self.valid_value(new_value)
            and self.initial_grid[y, x] == 0 
        ):
            self.grid[y, x] = new_value

    def clean_cell(self, x: int, y: int) -> None:
        """
        Clear a cell in the Sudoku grid, setting its value to 0.

        Parameters
        ----------
        x : int
            Column index.
        y : int
            Row index.
        """
        self.set_cell(x, y, 0)

    def check_rows(self) -> bool:
        """
        Check all rows in the Sudoku grid to ensure they contain unique values from 1 to 9.

        Returns
        -------
        bool
            True if all rows are valid, False otherwise.
        """
        for row in self.grid:
            s_row = set(row)
            if len(s_row) != 9 or 0 in s_row:
                return False
            return True

    def check_cols(self) -> bool:
        """
        Check all columns in the Sudoku grid to ensure they contain unique values from 1 to 9.

        Returns
        -------
        bool
            True if all columns are valid, False otherwise.
        """
        transposed_grid = self.grid.T
        for col in transposed_grid:
            s_col = set(col)
            if len(s_col) != 9 or 0 in s_col:
                return False
            return True

    def check_squares(self) -> bool:
        """
        Check all 3x3 squares in the Sudoku grid to ensure they contain unique values from 1 to 9.

        Returns
        -------
        bool
            True if all squares are valid, False otherwise.
        """
        for i in range(9):
            square = self.get_square(i)
            s_square = set(square.flatten())
            if len(s_square) != 9 or 0 in square:
                return False
        return True

    def is_solved(self) -> bool:
        """
        Determine if the Sudoku puzzle is solved by checking rows, columns, and squares.

        Returns
        -------
        bool
            True if the puzzle is solved, False otherwise.
        """
        return self.check_rows() and self.check_cols() and self.check_squares()

    def get_col(self, index: int) -> np.array:
        """
        Retrieve a column from the Sudoku grid.

        Parameters
        ----------
        index : int
            The index of the column to retrieve.

        Returns
        -------
        np.array
            The specified column as a NumPy array.
        """
        return self.grid[:, index]

    def get_row(self, index: int) -> np.array:
        """
        Retrieve a row from the Sudoku grid.

        Parameters
        ----------
        index : int
            The index of the row to retrieve.

        Returns
        -------
        np.array
            The specified row as a NumPy array.
        """
        return self.grid[index, :]

    def get_square(self, index: int) -> np.array:
        """
        Retrieve a 3x3 square from the Sudoku grid based on its index.

        Parameters
        ----------
        index : int
            The index of the square, ranging from 0 (top-left) to 8 (bottom-right).

        Returns
        -------
        np.array
            The specified 3x3 square as a NumPy array.
        """
        x = (index % 3) * 3
        y = (index // 3) * 3
        return self.grid[y : y + 3, x : x + 3]

    def get_hash(self) -> str:
        """
        Generate a hash string representing the current state of the Sudoku grid.

        Returns
        -------
        str
            The hash string of the current Sudoku grid.
        """
        output = ""
        for row in self.grid:
            for i in row:
                output += str(i)
        
        return output

    def __str__(self) -> str:
        """
        Create a string representation of the current state of the Sudoku grid.

        Returns
        -------
        str
            The string representation of the Sudoku grid.
        """
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
        """
        Create a colored string representation of the current state of the Sudoku grid,
        highlighting initial values in red.

        Returns
        -------
        str
            The colored string representation of the Sudoku grid.
        """
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
