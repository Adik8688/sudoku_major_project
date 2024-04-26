import pygame

BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
DEFAULT_FONT = "comicsans"


class Button:
    def __init__(self, x, y, width, height, text, on_click, border_width=2):
        self.rect = pygame.Rect(
            x + border_width,
            y + border_width,
            width - 2 * border_width,
            height - 2 * border_width,
        )
        self.border_rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.on_click = on_click
        self.font = pygame.font.SysFont(DEFAULT_FONT, 30)
        self.text_surf = self.font.render(self.text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.border_width = border_width
        self.border_color = BLACK
        self.button_color = GRAY

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.border_rect)
        pygame.draw.rect(surface, self.button_color, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def handle_click(self, x, y):
        if self.rect.collidepoint(x, y):
            self.on_click()
