import pygame
from .components.Cell import Cell
from .components.Mark import Mark
from .components.Button import Button
from .components.Slider import Slider

from .Sudoku import Sudoku
from .SudokuSolver import SudokuSolver
from src.SudokuDB import SudokuDB

import time

WIN_WIDTH = 450
WIN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (225, 122, 122)
REDGRAY = (255, 189, 189)
DARKBLUE = (0, 0, 139)
DEFAULT_FONT = "comicsans"
TITLE = "Sudoku by AD"
CELL_SIZE = 50
SOLVING_TIME = 10


class Game:
    def __init__(self):
        self.sudoku = Sudoku()

        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(TITLE)

        self.mark = Mark()
        self.shift_held = False

        self.cells = self.set_cells()

        self.solution = None
        self.step = 0
        self.solving_animation = False

        self.buttons = [
            Button(0, 450, 225, 75, "Clean", self.clean_grid),
            Button(0, 525, 225, 75, "Solve", self.solve_grid_animation),
            Button(225, 450, 225, 75, "Generate", self.generate_grid),
        ]
        self.slider = Slider(250, 550, 175, 30, 1, 10)


    def clean_grid(self):
        self.sudoku = Sudoku()
        self.cells = self.set_cells()

    def solve_grid(self):
        solver = SudokuSolver(self.sudoku)
        solved_sudoku = solver.solve()
        self.sudoku = solved_sudoku
        self.cells = self.set_cells()

    def solve_grid_animation(self):
        if not self.solving_animation and self.solution is None:
            solver = SudokuSolver(self.sudoku)
            solver.solve()
            self.solving_animation = True

    def generate_grid(self):
        print("Generating grid...")
        difficulty_level = self.slider.current_value

        db = SudokuDB()
        grid = db.get_sudoku_by_diff_2(difficulty_level)
        self.sudoku = Sudoku(grid)
        self.cells = self.set_cells()

    def set_cells(self):
        initial_grid = self.sudoku.initial_grid
        grid = self.sudoku.grid

        cells = []
        for y in range(9):
            row = []
            for x in range(9):
                immutable = initial_grid[y][x] != 0
                row.append(Cell(x, y, grid[y][x], 50, immutable))
            cells.append(row)
        return cells

    def run(self):
        run = True
        while run:
            run = self.is_run()
            if self.solving_animation:
                self.make_step()
            self.control()
            self.draw_game()
            self.update()

    def make_step(self):
        if self.solution is None:
            with open("output_solver.txt") as f:
                self.solution = list(f.readlines())

        if self.step >= len(self.solution):
            self.solving_animation = False
            self.step = 0
            self.solution = None
            return


        step = self.solution[self.step]
        x, y, value, n = step.split()

        self.mark.change_pos(int(x), int(y))
        self.put_number(int(value))
        self.step += 1

        time.sleep(SOLVING_TIME / len(self.solution))
        
 
    def control(self):
        keys = pygame.key.get_pressed()

        self.shift_held = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]


        actions = {
            pygame.K_w: lambda: self.mark.move(0, -1),
            pygame.K_UP: lambda: self.mark.move(0, -1),
            pygame.K_s: lambda: self.mark.move(0, 1),
            pygame.K_DOWN: lambda: self.mark.move(0, 1),
            pygame.K_d: lambda: self.mark.move(1, 0),
            pygame.K_RIGHT: lambda: self.mark.move(1, 0),
            pygame.K_a: lambda: self.mark.move(-1, 0),
            pygame.K_LEFT: lambda: self.mark.move(-1, 0),
            pygame.K_BACKSPACE: lambda: self.put_number(0)
        }

        for number in range(1, 10):
            actions[getattr(pygame, f'K_{number}')] = self.make_put_number_action(number)
            actions[getattr(pygame, f'K_KP{number}')] = self.make_put_number_action(number)


        for key, action in actions.items():
            if keys[key]:
                action()

        if pygame.mouse.get_pressed()[0]:
            self.handle_mouse_click(*pygame.mouse.get_pos())

           

    def make_put_number_action(self, number):
        def action():
            self.put_number(number)
        return action
    
    def handle_mouse_click(self, x, y):
        x_cor, y_cor = x // CELL_SIZE, y // CELL_SIZE
        self.mark.change_pos(x_cor, y_cor)
        for b in self.buttons:
            b.handle_click(x, y)

    
    def put_number(self, value):
        x_cor, y_cor = self.mark.get_coords()
        this_spot = self.cells[y_cor][x_cor]
        if this_spot.immutable:
            return
        
        if self.shift_held:
            this_spot.value = 0
            if value in this_spot.suspected_values:
                this_spot.suspected_values.remove(value)
            else:
                this_spot.suspected_values.append(value)
            return

        
        this_spot.suspected_values = []
        this_spot.value = value
        self.sudoku.set_cell(x_cor, y_cor, value)

        for i in range(9):
            if value in self.cells[self.mark.y_cor][i].suspected_values:
                self.cells[self.mark.y_cor][i].suspected_values.remove(value)
            if value in self.cells[i][self.mark.x_cor].suspected_values:
                self.cells[i][self.mark.x_cor].suspected_values.remove(value)

        for row in self.cells:
            for spot in row:
                if spot.square_id == this_spot.square_id:
                    if value in spot.suspected_values:
                        spot.suspected_values.remove(value)

    def draw_game(self):
        self.window.fill(WHITE)
        self.draw_numbers()
        self.draw_grid()
        self.draw_mark()
        self.draw_buttons()
        self.slider.draw(self.window)

    def draw_numbers(self):
        for y_cor, row in enumerate(self.cells):
            for x_cor, spot in enumerate(row):
                color = WHITE
                if ((x_cor == self.mark.x_cor or y_cor == self.mark.y_cor) and not (
                        x_cor == self.mark.x_cor and y_cor == self.mark.y_cor)) or spot.square_id == \
                        self.cells[self.mark.y_cor][
                            self.mark.x_cor].square_id:
                    color = GRAY
                if spot.is_collide(self.cells):
                    if color == GRAY:
                        color = REDGRAY
                    else:
                        color = RED

                self.draw_spot(spot, color)

    def draw_spot(self, spot, color):
        pygame.draw.rect(self.window, color, (spot.x * spot.size, spot.y * spot.size, spot.size, spot.size))
        if spot.value != 0:
            optimal_font_size = self.calculate_optimal_font_size(spot.size)
            font = pygame.font.SysFont(DEFAULT_FONT, optimal_font_size)
            number = font.render(str(spot.value), True, DARKBLUE if spot.immutable else BLACK)
            text_rect = number.get_rect(center=(spot.x * spot.size + spot.size/2, spot.y * spot.size + spot.size/2))
            self.window.blit(number, text_rect)

        if spot.suspected_values:
            optimal_small_font_size = self.calculate_optimal_font_size(spot.size, small=True)
            small_font = pygame.font.SysFont(DEFAULT_FONT, optimal_small_font_size)
            for number in spot.suspected_values:
                value = small_font.render(str(number), True, BLACK)
                self.window.blit(value, (spot.x * spot.size + spot.numbers_cor[number][0], spot.y * spot.size + spot.numbers_cor[number][1]))

    def calculate_optimal_font_size(self, box_size, small=False):
        base_font_size = 50 
        if small:
            base_font_size = base_font_size * 0.3

        return int(base_font_size * box_size // 50)

    def draw_mark(self):
        pygame.draw.polygon(self.window, RED, [(self.mark.x_cor * 50, self.mark.y_cor * 50), (
            (self.mark.x_cor + 1) * 50, self.mark.y_cor * 50), ((self.mark.x_cor + 1) * 50, (self.mark.y_cor + 1) * 50),
                                               (self.mark.x_cor * 50, (self.mark.y_cor + 1) * 50)], 8)

    def draw_grid(self):
        for i in range(WIN_WIDTH // 50 + 1):
            if i % 3 == 0:
                pygame.draw.line(self.window, (0, 0, 0), (i * 50, 0), (i * 50, WIN_WIDTH), 4)
                pygame.draw.line(self.window, (0, 0, 0), (0, i * 50), (WIN_WIDTH, i * 50), 4)
            else:
                pygame.draw.line(self.window, (0, 0, 0), (i * 50, 0), (i * 50, WIN_WIDTH), 2)
                pygame.draw.line(self.window, (0, 0, 0), (0, i * 50), (WIN_WIDTH, i * 50), 2)

    def draw_buttons(self):
        for b in self.buttons:
            b.draw(self.window)

    @staticmethod
    def update():
        pygame.time.delay(60)
        pygame.time.Clock().tick(60)
        pygame.display.update()

    def is_run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            self.slider.handle_event(event)
        return True
