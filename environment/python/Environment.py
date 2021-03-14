#! /usr/bin/env python

import pygame
import pool_of_water
from pygame.locals import *

BGColour  = (255, 255, 255)
width     = 20
height    = 12
size      = 500 / width
running   = True

#  Objects
screen = pygame.display.set_mode((size*width-1, size*height-1))
pygame.display.set_caption('My Universe')
clock = pygame.time.Clock()
pool = pool_of_water.Pool(width, height)
    
while running:
#for n in range(400):
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            pool.OutputData(pygame.mouse.get_pos(), size)
    
    #  Graphical Stuff
    screen.fill(BGColour)
    displayData = pool.GetDisplay('pressure')
    
    for x in range(width):
        for y in range(height):
            pygame.draw.rect(screen, displayData[x][y], (x*size, y*size, size, size),0)
            
            if x > 0:
                arrowSize = pool.dHorizontal[x-1][y] * 50
                if arrowSize > 0.5 or arrowSize < -0.5:
                    x1 = x*size+arrowSize-1
                    x2 = x*size-arrowSize-1
                   # pygame.draw.line(screen, BGColour, (x1, (y+0.5)*size-arrowSize), (x2, (y+0.5)*size))
                   # pygame.draw.line(screen, BGColour, (x1, (y+0.5)*size+arrowSize), (x2, (y+0.5)*size))
                
            if y > 0:
                arrowSize = pool.dVertical[x][y-1] * 50
                if arrowSize > 0.5 or arrowSize < -0.5:
                    y1 = y*size-1+arrowSize
                    y2 = y*size-1-arrowSize
                   # pygame.draw.line(screen, BGColour, ((x+0.5)*size-arrowSize, y1), ((x+0.5)*size, y2))
                   # pygame.draw.line(screen, BGColour, ((x+0.5)*size+arrowSize, y1), ((x+0.5)*size, y2))    
    
    pygame.display.flip()
   # if n%2 == 1:
    #    pygame.image.save(screen, 'Movie/env_%d.png' % n)

    #  Calculations    
    pool.Diffusion()
    pool.Gravity()
    #clock.tick(500)