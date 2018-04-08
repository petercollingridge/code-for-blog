#!/usr/bin/python
import random
import pygame
from pygame import *

try:
    import psyco
    psyco.full()
except ImportError:
    pass

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
            self.sugarSpreads()

    def sugarDecays(self):
        if random.random() < 0.1 * (self.sugar - self.nutrients):
            self.sugar -= random.randint(1, self.sugar)

    def sugarSpreads(self):
        if random.random() < 0.01 * self.sugar:
            spread_to_sector = random.choice(self.neighbours)
            spread_to_sector.sugar += random.randint(1,5)

class Agent():
    moves = [(-1, 0),(1, 0),(0, -1),(0, 1)]
    MAX_HUNGER = 4

    def __init__(self, sex, sector):
        self.age = 18
        self.sex = sex
        self.sector = sector
        self.threshold = random.randint(1,12)
        self.hunger = 0
        self.sugar = 0
        self.carrying_capacity = 4
        self.emptySector = False
        self.pregnant = False
        self.time_since_replication = 0

    def update(self):
        self.time_since_replication += 1
        self.hunger += 1
        if self.hunger > self.MAX_HUNGER:
            self.hunger = self.MAX_HUNGER

        self.eat()

        if self.emptySector:
            self.searchSurroundings()
        elif self.hunger == 0:
            if self.sector.sugar < self.threshold:
                self.searchSurroundings()
            elif self.time_since_replication > 200 and random.random() < 0.020:
                self.time_since_replication = 0
                self.pregnant = True
                self.hunger = 2
        else:
            self.collectSugar()

    def searchSurroundings(self):
        """ Look at the neighbouring sectors for the highest food and move there"""

        max = -1
        for sector in self.sector.neighbours:
            if sector.sugar > max:
                max = sector.sugar
                move_sector = sector

        self.sector = move_sector
        self.emptySector = False

    def collectSugar(self):
        collect = 2
        if collect > self.sector.sugar:
            collect = self.sector.sugar
            self.emptySector = True
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
        self.sector_update_time = 12

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
                    if 0 <= x+dx < self.width and 0 <= y+dy < self.height:
                        self.sectors[y][x].neighbours.append(self.sectors[y+dy][x+dx])

    def addNutrients(self, (gx, gy), amount, gradient):
        curvature = 4
        for x in range(self.width):
            for y in range(self.height):
                d = distance(x, y, gx, gy)
                self.sectors[y][x].nutrients += curvature * amount / (gradient * d + curvature)

    def update(self):
        self.time += 1

        if self.time % self.sector_update_time == 0:
            print self.time, len(self.agents)
           # timeline.write("%s\t%s\n" % (self.time, len(self.agents)))

            for x in range(0,self.width):
                for y in range(0,self.height):
                    self.sectors[y][x].update()

        for agent in self.agents:
            status = agent.update()

        n = 0
        while n < len(self.agents):
            if self.agents[n].hunger == Agent.MAX_HUNGER:
                del self.agents[n]
            else:
                if self.agents[n].pregnant:
                    self.agents[n].pregnant = False
                    sex = random.choice(['M', 'F'])
                    self.agents.append(Agent(sex, self.agents[n].sector))
                n += 1

    def display(self, surface):
        sizeX = surface.get_width() / self.width
        sizeY = surface.get_height() / self.height

        for x in range(self.width):
            for y in range(self.height):
                colour = (0, self.sectors[y][x].sugar, 0)
                #colour = (0, self.sectors[y][x].nutrients, 0)
                pygame.draw.rect(screen, colour, (x*sizeX, y*sizeY, sizeX, sizeY), 0)

        for agent in self.agents:
            if agent.sex == 'M':
                colour = (0, 0, 255 - 50*agent.hunger)
            else:
                colour = (255 - 50*agent.hunger, 0, 0)
            x = agent.sector.pos[0] * sizeX + sizeX/2
            y = agent.sector.pos[1] * sizeY + sizeY/2
            pygame.draw.circle(screen, colour, (x, y), 3, 0)

def InitialiseWorld(world):
  #  world.addNutrients((50, 8), 220, 3.2)
   # world.addNutrients((12, 24), 120, 0.8)
    world.addNutrients((35, 6), 220, 4)
    world.addNutrients((12, 24), 120, 1)

    for n in range(40):
        x = random.randint(0, world.width-1)
        y = random.randint(0, world.height-1)
        sex = random.choice(['M', 'F'])
        world.agents.append(Agent(sex, world.sectors[y][x]))

width, height = 400, 320
screen = pygame.display.set_mode((width, height))
screen.fill((255,255,255))

world = World(width/8, height/8)
InitialiseWorld(world)
#timeline = open('timeline.txt', 'w')

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    world.update()
    #world.display(screen)
    #pygame.display.flip()