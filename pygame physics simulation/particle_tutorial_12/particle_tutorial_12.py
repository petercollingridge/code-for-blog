import random
import pygame
import PyParticles

(width, height) = (400, 400)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Star formation')

universe = PyParticles.Environment((width, height))
universe.colour = (0,0,0)
universe.addFunctions(['move', 'attract', 'combine'])

def calculateRadius(mass):
    return 0.5 * mass ** (0.5)

for p in range(100):
    particle_mass = random.randint(1,4)
    particle_size = calculateRadius(particle_mass)
    universe.addParticles(mass=particle_mass, size=particle_size, speed=0, colour=(255,255,255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    universe.update()
    screen.fill(universe.colour)
    
    particles_to_remove = []
    for p in universe.particles:
        if 'collide_with' in p.__dict__:
            particles_to_remove.append(p.collide_with)
            p.size = calculateRadius(p.mass)
            del p.__dict__['collide_with']

        if p.size < 2:
            pygame.draw.rect(screen, p.colour, (int(p.x), int(p.y), 2, 2))
        else:
            pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), int(p.size), 0)
    
    for p in particles_to_remove:
        universe.particles.remove(p)

    pygame.display.flip()