class Mark:
    def __init__(self):
        self._x_cor = 4
        self._y_cor = 4

    @property
    def x_cor(self):
        return self._x_cor

    @x_cor.setter
    def x_cor(self, value):
        if 0 <= value <= 8:
            self._x_cor = value

    @property
    def y_cor(self):
        return self._y_cor

    @y_cor.setter
    def y_cor(self, value):
        if 0 <= value <= 8:
            self._y_cor = value


    def move(self, dx, dy):
        new_x_cor = self.x_cor + dx
        new_y_cor = self.y_cor + dy

        if 0 <= new_x_cor <= 8 and 0 <= new_y_cor <= 8:
            self.x_cor = new_x_cor
            self.y_cor = new_y_cor

    def change_pos(self, x, y):
        if 0 <= x <= 8 and 0 <= y <= 8:
            self.x_cor = x
            self.y_cor = y

    def get_coords(self):
        return (self.x_cor, self.y_cor)