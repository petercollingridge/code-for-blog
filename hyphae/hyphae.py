import pygame
import random
import math
import time

background_colour = (0, 0, 0)
(width, height) = (400, 360)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hyphae 1.1')
screen.fill(background_colour)


class GrowingPoint:
    speed = 0.15
    colour = (200, 113, 55)

    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.curve = random.uniform(0.001, 0.005) * random.choice([-1, 1])
        self.prob_turn = 0.005

    def move(self):
        self.angle += self.curve

        if random.random() < self.prob_turn:
            self.curve = random.uniform(0.001, 0.005) * random.choice([-1, 1])

        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed


growing_points = [GrowingPoint(width / 4, height - 60, math.pi / 4)]
prob_split = 0.0025

running = True
living = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            living = True

    if living:
        for g in growing_points:
            if random.random() < prob_split:
                new_growth = GrowingPoint(g.x, g.y, g.angle + math.pi / 4)
                new_growth.curve = - g.curve
                growing_points.append(new_growth)
                g.angle -= math.pi / 4

        for g in growing_points:
            g.move()
            if 0 < g.x < width and 0 < g.y < height:
                (cr, cg, cb, a) = screen.get_at((int(g.x), int(g.y)))
                if cr < 254:
                    (cr, cb, cg) = (cr + 2, cb + 2, cg + 2)
                screen.set_at((int(g.x), int(g.y)), (cr, cg, cb))

    pygame.display.flip()
    time.sleep(0.005)
