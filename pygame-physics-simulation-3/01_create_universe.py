import pygame

BACKGROUND_COLOR = (255, 255, 255)
(WIDTH, HEIGHT) = (300, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tutorial 1')
screen.fill(BACKGROUND_COLOR)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
