import pygame

BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
DEFAULT_FONT = "comicsans"


class Button:
    """
    A simple button class for pygame applications that handles drawing and click events.

    Attributes
    ----------
    rect : pygame.Rect
        The inner rectangle of the button which defines the clickable area.
    border_rect : pygame.Rect
        The outer rectangle of the button which includes the border.
    text : str
        The text displayed on the button.
    on_click : function
        The function to execute when the button is clicked.
    font : pygame.font.Font
        The font used for the button's text.
    text_surf : pygame.Surface
        The surface containing the rendered text.
    text_rect : pygame.Rect
        The rectangle defining the position of the text within the button.
    border_width : int
        The width of the button's border.
    border_color : tuple
        The color of the button's border, default is black.
    button_color : tuple
        The background color of the button, default is gray.
    """
    def __init__(self, x, y, width, height, text, on_click, border_width=2):
        """
        Initializes the button with its properties and layout.

        Parameters
        ----------
        x : int
            The x-coordinate of the button's top-left corner.
        y : int
            The y-coordinate of the button's top-left corner.
        width : int
            The width of the button.
        height : int
            The height of the button.
        text : str
            The text to display on the button.
        on_click : function
            The callback function to call when the button is clicked.
        border_width : int, optional
            The width of the button's border, default is 2 pixels.
        """
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
        """
        Draws the button on the specified surface.

        Parameters
        ----------
        surface : pygame.Surface
            The surface on which to draw the button.
        """
        pygame.draw.rect(surface, self.border_color, self.border_rect)
        pygame.draw.rect(surface, self.button_color, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def handle_click(self, x, y):
        """
        Handles mouse click events, determining if the click occurred within the button's boundaries and
        triggering the associated callback if it did.

        Parameters
        ----------
        x : int
            The x-coordinate of the mouse click.
        y : int
            The y-coordinate of the mouse click.
        """
        if self.rect.collidepoint(x, y):
            self.on_click()
