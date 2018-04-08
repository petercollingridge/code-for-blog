#!/usr/bin/python
import random
import pygame
from pygame import *

DIRECTIONS = [(-1, 0),(1, 0),(0, -1),(0, 1)]

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2) ** 0.5

class Sector():
    spreadRange =[-2, -1, 0, 1, 2]

    def __init__(self, x, y):
        self.pos = (x, y)
        self.neighbours = []
        self.nutrients = 0
        self.setSugar(0.5, 40)

    def setSugar(self, threshold, amount):
        if random.random() > threshold:
            self.sugar = random.randint(1, amount)
        else:
            self.sugar = 0

    def update(self):
        if self.sugar > self.nutrients:
            self.sugarDecays()
        else:
            return self.sugarSpreads()

    def sugarDecays(self):
        if random.random() < 0.1 * (self.sugar - self.nutrients):
            self.sugar -= random.randint(1, self.sugar)

    def sugarSpreads(self):      
        if random.random() < 0.01 * self.sugar:
            spread_to_sector = random.choice(self.neighbours)
            spread_to_sector.sugar += random.randint(1,5)
            x = random.choice(self.spreadRange)
            y = random.choice(self.spreadRange)
            return(x,y)

class Agent():
    moves = [(-1, 0),(1, 0),(0, -1),(0, 1)]
    MAX_HUNGER = 5

    def __init__(self, x, y, sector):
        self.x = x
        self.y = y
        self.sector = sector
        self.threshold = random.randint(1,8)
        self.hunger = 0
        self.sugar = 0
        self.carrying_capacity = 4

    def update(self):
        self.hunger += 1
        if self.hunger > self.MAX_HUNGER: self.hunger = self.MAX_HUNGER
        self.eat()

        if self.sector.sugar < self.threshold:
            self.move()
        else:
            self.collectSugar()

    def move(self):
        (dx, dy) = random.choice(self.moves)
        self.x += dx
        self.y += dy

    def collectSugar(self):
        collect = 2
        if collect > self.sector.sugar:
            collect = self.sector.sugar
        if collect + self.sugar > self.carrying_capacity:
            collect = self.carrying_capacity - self.sugar

        self.sugar += collect
        self.sector.sugar -= collect

    def eat(self):
        for n in range(2):
            if self.sugar > 0 and self.hunger > 0:
                self.hunger -= 1
                self.sugar -= 1

class World():
    """ Holds and displays a grid of sectors that agents explore """

    def __init__(self, x, y):
        self.width = x
        self.height = y
        self.createSectors()
        self.agents = []
        self.time = 0
        self.sector_update_time = 16

    def createSectors(self):
        self.sectors = []
        for y in range(self.height):
            sector_row = []
            for x in range(self.width):
                sector_row.append(Sector(x, y))
            self.sectors.append(sector_row)

        for x in range(self.width):
            for y in range(self.height):
                for (dx, dy) in DIRECTIONS:
                    if 0 < x+dx < self.width and 0 < y+dy < self.height:
                        self.sectors[y][x].neighbours.append(self.sectors[y+dy][x+dx])

    def addNutrients(self, (gx, gy), amount, gradient):
        curvature = 4
        for x in range(self.width):
            for y in range(self.height):
                d = distance(x, y, gx, gy)
                self.sectors[y][x].nutrients += curvature * amount / (gradient * d + curvature)

    def update(self):
        self.time += 1

        if self.time % self.sector_update_time  == 0:
            self.updateSectors()
        self.updateAgents()

    def updateSectors(self):
        for x in range(0,self.width):
            for y in range(0,self.height):
                spread = self.sectors[y][x].update()
                if spread != None:
                    self.spreadSugar(x, y, spread)

    def updateAgents(self):
        for agent in self.agents:
            agent.update()
            if agent.x < 0: agent.x = 0
            if agent.y < 0: agent.y = 0
            if agent.x >= self.width: agent.x = self.width-1
            if agent.y >= self.height: agent.y = self.height-1
            agent.sector = self.sectors[agent.y][agent.x]

    def spreadSugar(self, x, y, (sx, sy)):
        if -1 < x + sx < self.width and -1 < y + sy < self.height:
            self.sectors[y+sy][x+sx].sugar += random.randint(1,4)

    def display(self, surface):
        sizeX = surface.get_width() / self.width
        sizeY = surface.get_height() / self.height

        for x in range(self.width):
            for y in range(self.height):
                colour = (0, self.sectors[y][x].sugar, 0)
                #colour = (0, self.sectors[y][x].nutrients, 0)
                pygame.draw.rect(screen, colour, (x*sizeX, y*sizeY, sizeX, sizeY), 0)

        for agent in self.agents:
            colour = (255 - 50*agent.hunger, 0, 0)
            pygame.draw.circle(screen, colour, (agent.x*sizeX+sizeX/2, agent.y*sizeY+sizeY/2), 3, 0)

def InitialiseWorld(world):
    world.addNutrients((50, 10), 220, 3.2)
    world.addNutrients((12, 24), 120, 0.8)

    for n in range (20):
        x = random.randint(0, world.width-1)
        y = random.randint(0, world.height-1)
        world.agents.append(Agent(x, y, world.sectors[y][x]))

width, height = 600, 400
screen = pygame.display.set_mode((width, height))
screen.fill((255,255,255))

world = World(width/10, height/10)
InitialiseWorld(world)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    world.update()
    world.display(screen)
    pygame.display.flip()