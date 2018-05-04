#! /usr/bin/env python

#   -To do-
#   Ability to centre screen on universe's centre of mass
#   Zoom in and out?
#   Control speed, taking into account computational time

import math
import random
import pygame
from pygame import *

def combineVectors((angle1, length1), (angle2, length2)):
    """ Adds together two vectors given as an angle plus a magnitude (length)"""

    x  = math.sin(angle1) * length1
    y  = math.cos(angle1) * length1
    x1 = x + math.sin(angle2) * length2
    y1 = y + math.cos(angle2) * length2
    
    angle = 0.5*math.pi - math.atan2(y1, x1)
    length  = math.hypot(x1, y1)
    return (angle, length)

class Particle():
    def __init__(self, x, y, mass=1):
        self.x = x
        self.y = y
        self.mass = mass
        self.findRadius()

        self.speed = 0
        self.angle = 0

    def findRadius(self):
        self.radius = 0.4 * self.mass ** (1.0/3.0)
        self.size = int(self.radius)
        if self.size < 2:
            self.colour = (100+self.mass, 100+self.mass, 100+self.mass)
        else:
            self.colour = (255,255, 0)

    def move(self):
        """ Moves the particle based on its speed and direction """
 
        self.x += math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed

    def attract(self, other):
        """" Particles attract one another based on their distance and masses"""
        
        dx = (self.x - other.x) * 2
        dy = (self.y - other.y) * 2

        dist  = math.hypot(dx, dy)
        force = 0.1 * self.mass * other.mass / dist**2
        theta = 0.5 * math.pi - math.atan2(dy, dx)    
        
        if dist < self.radius + other.radius:
            total_mass = self.mass + other.mass

            self.x = (self.x * self.mass + other.x * other.mass) / total_mass
            self.y = (self.y * self.mass + other.y * other.mass) / total_mass
            self.speed = self.speed * self.mass / total_mass
            other.speed = other.speed * other.mass / total_mass

            (self.angle,  self.speed)  = combineVectors((self.angle,  self.speed), (other.angle, other.speed))

            self.mass = total_mass
            self.findRadius()
            return other
        else:
            (self.angle,  self.speed)  = combineVectors((self.angle,  self.speed),  (theta+math.pi, force/self.mass))
            (other.angle, other.speed) = combineVectors((other.angle, other.speed), (theta, force/other.mass))

#   Set up Pygame variables
pygame.init()
BG_colour = (0,0,0)
particle_colour = (200,200,200)
(width, height) = (480, 360)
screen = pygame.display.set_mode((width, height))

number_of_particles = 170
particles = []

for p in range(number_of_particles):
    mass = random.randint(1, 4)
    #mass = 1
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    particles.append(Particle(x, y, mass))

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(BG_colour)

    for i in range(number_of_particles):
        j = i+1

        while j < number_of_particles:
            collide = particles[i].attract(particles[j])

            if collide != None:
                particles.remove(collide)
                number_of_particles -= 1
            else:
                j += 1

    for p in particles:
        p.move()

 #       if p.size < 1:
 #           screen.set_at((int(p.x), int(p.y)), particle_colour)
        if p.size < 2:
            pygame.draw.rect(screen, p.colour, (int(p.x), int(p.y), 2, 2))
        else:
            pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, 0)
      
    pygame.display.flip()

for p in particles:
    dx = math.sin(p.angle) * p.speed
    dy = math.cos(p.angle) * p.speed
    print "(%d, %d)\t(dx=%f, dy=%f)\tmass = %d" % (p.x, p.y, dx, dy, p.mass)
