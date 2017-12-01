'''
Created on Nov 28, 2017

@author: vince
'''

from random import random
import Gut

''' Internal parameters'''
replication_threshold = 1.2  # TBD
movement_cost = 0.5 #TBD
cdif_toxin_rate = 5
death_nutrients = 0
cdif_sporulate_threshold = 0.05
cdif_sporulate_chance = 0.15
cdif_vegetate_threshold = 0.1

gut = None

class Cell(object):
    '''
    This is a parent class for epithelial, commensal, and C dif cells
    '''
    basal_metabolic_cost = 0.2

    def __init__(self, energy):
        '''
        Constructor
        '''
        global gut
        if gut==None:
            gut=Gut.gut
        self.energy = energy
        self.is_mobile = False   #Cdif_Veg overrides
        
    def step(self):
        self.replicate()
        self.move()
        self.consume()
        self.checkHealth()
    
    def replicate(self):
        if self.energy > replication_threshold:
            #TBD is there energy expenditure in replication?
            spawn = self.__class__(self.energy/2)
            gut.spawn(spawn, gut.positionOf[self]) # TBD - where does spawn go?
            self.energy /= 2
    
    def move(self):
        if self.is_mobile:
            current_position = gut.positionOf[self]
            patches = gut.getNeighborhood(current_position)
            destination = max(patches, key=lambda patch: patch.nutrients)
            if gut.positionOf[destination] != current_position:
                gut.changePatch(self, destination)
                self.energy -= movement_cost
    
    def consume(self):
        (nutrient, TCA, DCA, toxin) = gut.getCompoundsAt(gut.positionOf[self])
        (nutrient, TCA, DCA, toxin) = self.processCompounds(nutrient, TCA, DCA, toxin)
        gut.putCompounds(gut.positionOf[self], nutrient, TCA, DCA, toxin)
        self.energy -= Cell.basal_metabolic_cost
    
    def checkHealth(self):
        '''
        '''
        if self.energy < 0:
            gut.removeAgent(self)
    
    def processCompounds(self, nutrient, TCA, DCA, toxin):
        '''
        Stub method; needs to be overridden by each subclass
        '''
        consumption = min(nutrient, 1)
        self.energy += consumption
        nutrient = -consumption
        return (nutrient, TCA, DCA, toxin)
    
class EpiCell(Cell):  
    
    def __init__(self, energy):
        super(EpiCell, self).__init__(energy)
    
    def checkHealth(self):
        if self.energy < 0:
            pos = gut.positionOf[self]
            gut.putCompounds(pos, death_nutrients, 0, 0, 0)
            gut.removeAgent(self)
    
    def replicate(self):
        if self.energy > replication_threshold:
            #TBD is there energy expenditure in replication?
            spawn = self.__class__(self.energy/2)
            (x,y) = gut.positionOf[self]
#             x += random()-0.5
#             y += random()-0.5
            gut.spawn(spawn, (x,y)) # TBD - where does spawn go?
            self.energy /= 2

class Commensal(Cell):  
    
    def __init__(self, energy):
        super(Commensal, self).__init__(energy)
    
class Cdif_Spore(Cell):  
    
    def __init__(self, energy):
        super(Cdif_Spore, self).__init__(energy)
    

class Cdif_Veg(Cell):  
    
    def __init__(self, energy):
        super(Cdif_Veg, self).__init__(energy)
        self.is_mobile = True
    
    def checkHealth(self):
        if self.energy < cdif_sporulate_threshold:
            if random() < cdif_sporulate_chance:
                self.sporulate()
            elif self.energy < 0:
                pos = gut.positionOf[self]
                gut.putCompounds(pos, death_nutrients, 0, 0, 0)
                gut.removeAgent(self)
    

            