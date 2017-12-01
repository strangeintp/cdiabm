'''
Created on Nov 29, 2017

@author: vince
'''

from cells import EpiCell
from cells import Commensal
from cells import Cdif_Spore
from cells import Cdif_Veg
from random import randint
from random import shuffle

'''Internal parameters'''
grid_size = 31
initial_energy = 0.5
initial_nutrient = 0.2

'''external parameters'''
initial_commensal_count = 200
initial_cdifspore_count = 0
nutrient_rate = 1
bile_rate = 100

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
            spore = Cdif_Spore(initial_energy)
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
        things = list(self.positionOf.keys())
        shuffle(things)
        for thing in things:
            thing.step()
    
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
        
class Patch(object):
    
    def __init__(self):
        self.nutrient = initial_nutrient
        self.TCA = 0
        self.DCA = 0
        self.toxin = 0
        
    def step(self):
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
        

        