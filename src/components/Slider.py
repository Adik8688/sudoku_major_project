import pygame

BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class Slider:
    def __init__(self, x, y, width, height, start_range, end_range):
        self.track_rect = pygame.Rect(x, y, width, height // 2)
        self.handle_rect = pygame.Rect(x, y - height // 4, height, height)
        self.handle_color = GRAY
        self.track_color = BLACK
        self.value_color = BLACK
        self.start_range = start_range
        self.end_range = end_range
        self.current_value = start_range
        self.font = pygame.font.SysFont("comicsans", 24)
        self.dragging = False  

    def draw(self, surface):
        pygame.draw.rect(surface, self.track_color, self.track_rect)
        pygame.draw.rect(surface, self.handle_color, self.handle_rect)
        value_surf = self.font.render(f"{self.current_value:.3f}", True, self.value_color)
        value_rect = value_surf.get_rect(center=(self.handle_rect.centerx, self.track_rect.bottom + 20))
        surface.blit(value_surf, value_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.move_handle(event.pos[0])

    def move_handle(self, mouse_x):
        new_x = max(self.track_rect.left, min(mouse_x - self.handle_rect.width // 2, self.track_rect.right - self.handle_rect.width))
        self.handle_rect.x = new_x
        self.update_value()

    def update_value(self):
        track_width = self.track_rect.width - self.handle_rect.width
        handle_pos = self.handle_rect.x - self.track_rect.x
        percentage = handle_pos / track_width
        value_range = self.end_range - self.start_range
        self.current_value = self.start_range + percentage * value_range
        self.current_value = round(self.current_value, 3)