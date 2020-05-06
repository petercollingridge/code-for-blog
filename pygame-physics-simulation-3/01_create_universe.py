import pygame

# Universe constants
BACKGROUND_COLOR = (255, 255, 255)
(WIDTH, HEIGHT) = (300, 200)

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tutorial 1')

# Display a blank screen
screen.fill(BACKGROUND_COLOR)
pygame.display.flip()

# Keep showing the window until the user closes it
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); 
