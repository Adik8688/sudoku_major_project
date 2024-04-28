class Mark:
    """
    Manages the position of a marker or cursor within a Sudoku grid, handling its movement and updating its coordinates.

    Attributes
    ----------
    _x_cor : int
        The current x-coordinate of the marker within the grid.
    _y_cor : int
        The current y-coordinate of the marker within the grid.
    """
    def __init__(self):
        """
        Initializes the Mark class with the marker positioned in the middle of the grid (position 4, 4).
        """
        self._x_cor = 4
        self._y_cor = 4

    @property
    def x_cor(self):
        """
        The x-coordinate property of the marker.

        Returns
        -------
        int
            The current x-coordinate of the marker.
        """
        return self._x_cor

    @x_cor.setter
    def x_cor(self, value):
        """
        Sets the x-coordinate of the marker ensuring it remains within the grid boundaries (0 to 8).

        Parameters
        ----------
        value : int
            The new x-coordinate of the marker.
        """
        if 0 <= value <= 8:
            self._x_cor = value

    @property
    def y_cor(self):
        """
        The y-coordinate property of the marker.

        Returns
        -------
        int
            The current y-coordinate of the marker.
        """
        return self._y_cor

    @y_cor.setter
    def y_cor(self, value):
        """
        Sets the y-coordinate of the marker ensuring it remains within the grid boundaries (0 to 8).

        Parameters
        ----------
        value : int
            The new y-coordinate of the marker.
        """
        if 0 <= value <= 8:
            self._y_cor = value


    def move(self, dx, dy):
        """
        Moves the marker by a specified amount in the x and y directions, if within grid boundaries.

        Parameters
        ----------
        dx : int
            The change in the x-direction.
        dy : int
            The change in the y-direction.
        """
        new_x_cor = self.x_cor + dx
        new_y_cor = self.y_cor + dy

        if 0 <= new_x_cor <= 8 and 0 <= new_y_cor <= 8:
            self.x_cor = new_x_cor
            self.y_cor = new_y_cor

    def change_pos(self, x, y):
        """
        Changes the position of the marker to specified coordinates if within grid boundaries.

        Parameters
        ----------
        x : int
            The new x-coordinate for the marker.
        y : int
            The new y-coordinate for the marker.
        """
        if 0 <= x <= 8 and 0 <= y <= 8:
            self.x_cor = x
            self.y_cor = y

    def get_coords(self):
        """
        Retrieves the current coordinates of the marker.

        Returns
        -------
        tuple
            A tuple containing the x and y coordinates (x_cor, y_cor) of the marker.
        """
        return (self.x_cor, self.y_cor)