import pygame
import sys

pygame.init()

window_size = (400, 400)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Sudoku")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # logic
            

    # refresh
    pygame.display.flip()

pygame.quit()
sys.exit()
