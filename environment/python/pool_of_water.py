#! /usr/bin/env python

NUM_ATOMS   = 1000
K_diffusion = 0.001
K_gravity   = 0.02
K_moveTemp  = 4.0
K_gravTemp  = 2.5
waterTemp   = 20
rockTemp    = 20
airTemp     = 20

class Sector:
    """ A sector in a simulated environment """    
    def __init__(self, temperature):
        self.atoms = NUM_ATOMS
        self.energy = temperature * self.atoms
        self.dAtoms = 0
        self.dTemperature = 0
    
    def CalculateDiffusion(self):
        self.dAtoms = self.energy * K_diffusion
        self.dEnergy = (self.energy + K_moveTemp * self.atoms) * (self.dAtoms / self.atoms)
    
    def CalculateGravity(self):
        self.dAtoms = self.atoms * self.atoms * K_gravity / self.energy
        self.dEnergy = (self.energy - K_gravTemp * self.atoms) * (self.dAtoms / self.atoms)
    
    def MoveTemp(self, temperature):
        """ Move the energy of a sector towards a passed temperature.
            Used to account for cooling or warming at a surface """
        self.energy -= self.dEnergy
        self.energy += self.dAtoms * (temperature + K_moveTemp)
    
    def MoveAtoms(self, other):
        """ Move the delta group of atoms from self to the passed sector """
        self.atoms  -= self.dAtoms
        self.energy -= self.dEnergy
        other.atoms  += self.dAtoms
        other.energy += self.dEnergy
    
class Pool:
    """ A matrix of water sectors """    
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.sectors     = []
        self.dHorizontal = []       # for arrows
        self.dVertical   = []
    
        for x in range(self.width):
            self.sectors.append([])
            self.dHorizontal.append([])
            self.dVertical.append([])
            for y in range(self.height):
                self.sectors[x].append(Sector(waterTemp))
                self.dHorizontal[x].append(0.0)
                self.dVertical[x].append(0.0)

    def Diffusion(self):
        for x in range(self.width):
            for y in range(self.height):
                self.sectors[x][y].CalculateDiffusion()
                if x > 0:
                    self.dHorizontal[x-1][y] = self.sectors[x][y].dAtoms - self.sectors[x-1][y].dAtoms
                    
                if y > 0:    
                    self.dVertical[x][y-1] = self.sectors[x][y].dAtoms - self.sectors[x][y-1].dAtoms

        for x in range(self.width):
            for y in range(self.height):
                if x > 0: self.sectors[x][y].MoveAtoms(self.sectors[x-1][y])
                else:       self.sectors[x][y].MoveTemp(rockTemp)
                if y > 0: self.sectors[x][y].MoveAtoms(self.sectors[x][y-1])
                else:     self.sectors[x][y].MoveTemp(airTemp)
                if x < self.width-1:  self.sectors[x][y].MoveAtoms(self.sectors[x+1][y])
                else:                 self.sectors[x][y].MoveTemp(rockTemp)
                if y < self.height-1: self.sectors[x][y].MoveAtoms(self.sectors[x][y+1])
                else:                 self.sectors[x][y].MoveTemp(rockTemp)

        #print "Flux %f atoms up (%f)" %(self.sectors[5][11].dAtoms-self.sectors[5][10].dAtoms, self.dVertical[5][10])
        self.sectors[5][self.height-1].MoveTemp(100)
    
    def Gravity(self):
        for x in range(self.width):
            for y in range(self.height-1):
                self.sectors[x][y].CalculateGravity()
                self.dVertical[x][y] -= self.sectors[x][y].dAtoms
                
        for x in range(self.width):
            for y in range(self.height-1):
                self.sectors[x][y].MoveAtoms(self.sectors[x][y+1])
                
    def OutputData(self, mouse_position, sector_size):
        (posX, posY) = mouse_position
        posX /= sector_size
        posY /= sector_size
        print "Sector (%d, %d): %f atoms; energy %f; temp %f" %(posX, posY, self.sectors[posX][posY].atoms, self.sectors[posX][posY].energy, self.sectors[posX][posY].energy / self.sectors[posX][posY].atoms)
    
    def GetDisplay(self, type):
        """ Loops through sectors and finds maximum and minimum values for a certain parameter (temperature for now)
            Then loops through and normalises all the parameters and converts to a colour based on the values """
    
        displayData = []
        minData = 1000000
        maxData = 0
        
        for x in range(self.width):
            displayData.append([])
            for y in range(self.height):
                if type == 'temperature':
                    data = self.sectors[x][y].energy / self.sectors[x][y].atoms
                elif type == 'pressure':
                    data = self.sectors[x][y].atoms
                displayData[x].append(data)
                
                if data < minData:
                    minData = data
                if data > maxData:
                    maxData = data

        if maxData - minData > 0:
            difference = maxData - minData
        else:
            difference = 1
        
        for x in range(self.width):
            for y in range(self.height):
        #        if displayData[x][y] < difference * 0.5 + minData:
        #            colourValue = 15 + 450 * (displayData[x][y] - minData) / difference
        #            displayData[x][y] = (0, 0, colourValue)
        #        else:
        #            colourValue = 225 * (displayData[x][y] - minData - difference*0.5) / (difference * 0.5)
        #            displayData[x][y] = (colourValue, colourValue, 255)
                if displayData[x][y] > difference * 0.5 + minData:
                    colourValue = 225 * (displayData[x][y] - minData - difference*0.5) / (difference * 0.5)
                    displayData[x][y] = (0, 0, 255-colourValue)
                else:
                    colourValue = 450 * (displayData[x][y] - minData) / difference
                    displayData[x][y] = (225-colourValue, 225-colourValue, 255)
        return displayData
