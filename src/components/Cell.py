class Cell:
    """
    Represents an individual cell in a Sudoku grid, handling its state and interactions.

    Attributes
    ----------
    size : int
        The size of the cell in pixels.
    x : int
        The x-coordinate of the cell within the grid.
    y : int
        The y-coordinate of the cell within the grid.
    square_id : int
        The identifier for the 3x3 square the cell belongs to.
    value : int
        The current value of the cell, where 0 represents an empty cell.
    suspected_values : list
        A list of candidate numbers that might fit in the cell (used for notes).
    immutable : bool
        A boolean indicating whether the cell's value is immutable (part of the initial puzzle setup).
    numbers_cor : dict
        A dictionary mapping candidate numbers to their positions within the cell for rendering purposes.
    """
    def __init__(self, x, y, value, size, immutable=False):
        """
        Initializes a new Cell with its location, value, and visual size.

        Parameters
        ----------
        x : int
            The x-coordinate of the cell in the Sudoku grid.
        y : int
            The y-coordinate of the cell in the Sudoku grid.
        value : int
            The numerical value of the cell, 0 if empty.
        size : int
            The size of the cell in pixels, used for drawing the cell.
        immutable : bool, optional
            Whether the cell's value is immutable (cannot be changed by the player), default is False.
        """
        self.size = size
        self.x = x
        self.y = y
        self.square_id = self.get_square(x, y)
        self.value = value
        self.suspected_values = []
        self.immutable = immutable
        self.numbers_cor = {1: (6, 0), 2: (22, 0), 3: (38, 0), 4: (6, 15), 5: (22, 15), 6: (38, 15), 7: (6, 31),
                            8: (22, 31), 9: (38, 31)}

    @staticmethod
    def get_square(x, y):
        """
        Calculates the identifier for the 3x3 square based on the cell's coordinates.

        Parameters
        ----------
        x : int
            The x-coordinate of the cell.
        y : int
            The y-coordinate of the cell.

        Returns
        -------
        int
            The index of the 3x3 square the cell belongs to, ranging from 0 to 8.
        """
        return (y // 3) * 3 + (x // 3)

    def is_pressed(self, x, y):
        """
        Determines if the cell has been clicked based on mouse coordinates.

        Parameters
        ----------
        x : int
            The x-coordinate of the mouse click.
        y : int
            The y-coordinate of the mouse click.

        Returns
        -------
        bool
            True if the click is within the cell's boundaries, False otherwise.
        """
        return self.x < x // self.size < self.x + self.size and self.y < y // self.size < self.y + self.size

    def is_collide(self, cells):
        """
        Checks if the current value of the cell conflicts with any other cell in its row, column, or square.

        Parameters
        ----------
        cells : list
            A 2D list of all cells in the Sudoku grid.

        Returns
        -------
        bool
            True if there is a conflict, False if there is no conflict.
        """

        if self.value == 0:
            return False

        for i in range(9):
            if i != self.y and self.value == cells[i][self.x].value:
                return True
            if i != self.x and self.value == cells[self.y][i].value:
                return True
        
        sq_x = self.square_id % 3
        sq_y = self.square_id // 3

        for y in range(3 * sq_y, 3 * sq_y + 3):
            for x in range(3 * sq_x, 3 * sq_x + 3):
                if self.y != y and self.x != x and cells[y][x].value == self.value:
                    return True

        return False