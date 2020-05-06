import pygame
pygame.init()

# Universe constants
BACKGROUND_COLOR = (255, 255, 255)
(WIDTH, HEIGHT) = (300, 200)

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tutorial 2')

# Display a blank screen with a particle on it
screen.fill(BACKGROUND_COLOR)

particle_colour = (0, 0, 255)
particle_position = (50, 30)
particle_size = 20
particle_thickness = 0

pygame.draw.circle(screen, particle_colour, particle_position, particle_size, particle_thickness)
pygame.display.flip()

# Keep showing the window until the user closes it
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
