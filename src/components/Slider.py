import pygame

BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class Slider:
    """
    A slider control that allows selecting a value by moving a handle along a track.

    Attributes
    ----------
    track_rect : pygame.Rect
        The rectangle representing the slider's track.
    handle_rect : pygame.Rect
        The rectangle representing the slider's handle.
    handle_color : tuple
        The color of the slider's handle.
    track_color : tuple
        The color of the slider's track.
    value_color : tuple
        The color used for the slider's value text.
    start_range : float
        The minimum value of the slider.
    end_range : float
        The maximum value of the slider.
    current_value : float
        The current value of the slider.
    font : pygame.font.Font
        The font used for rendering the slider's value.
    dragging : bool
        A flag indicating whether the slider's handle is currently being dragged.
    """
    def __init__(self, x, y, width, height, start_range, end_range):
        """
        Initializes a Slider object.

        Parameters
        ----------
        x : int
            The x-coordinate of the slider.
        y : int
            The y-coordinate of the slider.
        width : int
            The width of the slider.
        height : int
            The height of the slider.
        start_range : float
            The starting value of the slider's range.
        end_range : float
            The ending value of the slider's range.
        """
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
        """
        Draws the slider on a given surface.

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the slider on.
        """
        pygame.draw.rect(surface, self.track_color, self.track_rect)
        pygame.draw.rect(surface, self.handle_color, self.handle_rect)
        value_surf = self.font.render(f"{self.current_value:.3f}", True, self.value_color)
        value_rect = value_surf.get_rect(center=(self.handle_rect.centerx, self.track_rect.bottom + 20))
        surface.blit(value_surf, value_rect)


    def handle_event(self, event):
        """
        Handles mouse events to control the slider's handle and update the slider's value.

        Parameters
        ----------
        event : pygame.event.Event
            The event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.move_handle(event.pos[0])

    def move_handle(self, mouse_x):
        """
        Moves the handle to a new position based on mouse movements, ensuring it stays within the track.

        Parameters
        ----------
        mouse_x : int
            The x-coordinate of the mouse position.
        """
        new_x = max(self.track_rect.left, min(mouse_x - self.handle_rect.width // 2, self.track_rect.right - self.handle_rect.width))
        self.handle_rect.x = new_x
        self.update_value()

    def update_value(self):
        """
        Updates the current value of the slider based on the handle's position along the track.
        """
        track_width = self.track_rect.width - self.handle_rect.width
        handle_pos = self.handle_rect.x - self.track_rect.x
        percentage = handle_pos / track_width
        value_range = self.end_range - self.start_range
        self.current_value = self.start_range + percentage * value_range
        self.current_value = round(self.current_value, 3)