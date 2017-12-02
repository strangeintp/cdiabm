'''
Created on Nov 29, 2017

@author: vince
'''

from cells import EpiCell, Commensal, Cdif_Spore, Cdif_Veg
from random import randint, shuffle, sample, random
import scipy as SP

'''Internal parameters'''
grid_size = 31
initial_energy = 1.0
initial_nutrient = 0.5

'''external parameters'''
initial_commensal_count = (3*grid_size*grid_size)//1
initial_cdifspore_count = 200
nutrient_rate = 1
bile_rate = 0.01
kill_rate = 0.0

def Initial_commensals(count = (3*grid_size*grid_size)):
    global initial_commensal_count
    initial_commensal_count = int(count)
    return initial_commensal_count

def Initial_spores(count = 200):
    global initial_cdifspore_count
    initial_cdifspore_count = int(count)
    return initial_cdifspore_count

def Nutrient_replenish_rate(rate = 1.0):
    global nutrient_rate
    nutrient_rate = float(rate)
    return nutrient_rate

def Antiobiotic_kill_rate(rate = 0.0):
    global kill_rate
    kill_rate = float(rate)
    return kill_rate

def modulus((x,y)):
    return ((x%grid_size, y%grid_size))

gut = None

class Gut(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        global gut
        gut = self
        self.positionOf = {}
        self.patchAt = {}
        self.epicells = []
        self.commensals = []
        self.cdif_spores = []
        self.cdif_vegs = []
        
        ''' Initialize patches and epithelial cells'''
        num_patches = grid_size*grid_size
        for x in range(grid_size):
            for y in range(grid_size):
                patch = Patch()
                patch.nutrient = initial_nutrient #TBD - what is initial amount?
                self.positionOf[patch] = (x,y)
                self.patchAt[x,y] = patch
                cell = EpiCell(initial_energy)
                self.spawn(cell, (x,y))
        
        ''' Initialize commensals '''
        for i in range(initial_commensal_count):
            cell = Commensal(initial_energy)
            x = randint(0, grid_size-1)
            y = randint(0, grid_size-1)
            self.spawn(cell, (x,y))
        
        '''Initialize C dif spores'''
        for i in range(initial_cdifspore_count):
            spore = Cdif_Spore(initial_energy*random())
            x = randint(0, grid_size-1)
            y = randint(0, grid_size-1)
            self.spawn(spore, (x,y))
    
    def spawn(self, cell, (x,y), neighbors=False):
        if neighbors:
            x += randint(-1,1)
            y += randint(-1,1)
        self.positionOf[cell] = modulus((x,y))
        if isinstance(cell, EpiCell):
            self.epicells.append(cell)
        elif isinstance(cell, Commensal):
            self.commensals.append(cell)
        elif isinstance(cell, Cdif_Spore):
            self.cdif_spores.append(cell)
        elif isinstance(cell, Cdif_Veg):
            self.cdif_vegs.append(cell)
        
    def step(self):
        if kill_rate > 0:
            self.killCells(self.commensals)
            self.killCells(self.cdif_vegs)
        things = list(self.positionOf.keys())
        shuffle(things)
        for thing in things:
            thing.step()
    
    def killCells(self, cells):
        num_killed = int(len(cells)*kill_rate)
        kill_list = sample(cells, num_killed)
        for killed in kill_list:
            self.removeAgent(killed)
    
    def getNeighborhood(self, position):
        (x,y) = position
        patches = []
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                patches.append(self.patchAt[modulus((x+dx,y+dy))])
        return patches
    
    def changePatch(self, cell, patch):
        self.positionOf[cell] = self.positionOf[patch]
    
    def removeAgent(self, cell):
        self.positionOf.pop(cell, None)
        if isinstance(cell, EpiCell):
            self.epicells.remove(cell)
        elif isinstance(cell, Commensal):
            self.commensals.remove(cell)
        elif isinstance(cell, Cdif_Spore):
            self.cdif_spores.remove(cell)
        elif isinstance(cell, Cdif_Veg):
            self.cdif_vegs.remove(cell)
    
    def getCompoundsAt(self, position):
        patch = self.patchAt[position]
        compounds = (patch.nutrient, patch.TCA, patch.DCA, patch.toxin)
        patch.nutrient = 0
        patch.TCA = 0
        patch.DCA = 0
        patch.toxin = 0
        return compounds
    
    def putCompounds(self, position, nutrient, TCA, DCA, toxin):
        patch = self.patchAt[position]
        patch.nutrient += nutrient
        patch.TCA += TCA
        patch.DCA += DCA
        patch.toxin += toxin
    
    def health(self):
        health = SP.zeros([grid_size, grid_size])
        for cell in self.epicells:
            pos = self.positionOf[cell]
            health[pos] = cell.energy
        return health
        
class Patch(object):
    
    def __init__(self):
        self.nutrient = initial_nutrient
        self.TCA = 0
        self.DCA = 0
        self.toxin = 0
        
    def step(self):
        self.DCA *= 0.87
        self.secrete()
        self.diffuse()
    
    def secrete(self):
        self.nutrient += nutrient_rate
        self.TCA += bile_rate
    
    def diffuse(self):
        neighborhood = gut.getNeighborhood(gut.positionOf[self])
        nutrient = self.nutrient/9
        TCA = self.TCA/9
        DCA = self.DCA/9
        toxin = self.toxin/9
        self.nutrient = 0
        self.TCA = 0
        self.DCA = 0
        self.toxin = 0
        for patch in neighborhood:
            patch.nutrient += nutrient
            patch.TCA += TCA
            patch.DCA += DCA
            patch.toxin += toxin
        

        