class Cell:
    def __init__(self, x, y, value, size, immutable=False):
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
        return (y // 3) * 3 + (x // 3)

    def is_pressed(self, x, y):
        return self.x < x // self.size < self.x + self.size and self.y < y // self.size < self.y + self.size

    def is_collide(self, cells):

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


        # for row in cells:
        #     for cell in row:
        #         if cell.x == self.x and cell.y == self.y:
        #             continue

        #         if cell.value == self.value and self.value != 0:
        #             if cell.x == self.x or cell.y == self.y or cell.square_id == self.square_id:
        #                 return True
        return False