'''
Created on Nov 28, 2017

@author: vince
'''

from random import random
import Gut

''' Internal parameters'''
replication_threshold = 1.2
movement_cost = 0.4 #TBD
cdif_sporulate_threshold = 0.05
cdif_sporulate_chance = 0.15
cdif_germinate_threshold = 0.05
toxin_production = 0.05

class Cell(object):
    '''
    This is a parent class for epithelial, commensal, and C dif cells
    '''
    max_ID = 0

    def __init__(self, energy):
        '''
        Constructor
        '''
        self.ID = Cell.max_ID
        Cell.max_ID += 1
        self.energy = energy
        self.is_mobile = False   #Cdif_Veg overrides
        
    def step(self):
        if self.ID==0:
            pass #debug breakpoint
        self.replicate()
        self.move()
        self.consume()
        self.checkHealth()        
    
    def replicate(self):
        if self.energy > replication_threshold:
            #TBD is there energy expenditure in replication?
            spawn = self.__class__(self.energy/2)
            Gut.gut.spawn(spawn, Gut.gut.positionOf[self], neighbors=True) # TBD - where does spawn go?
            self.energy /= 2
    
    def move(self):
        if self.is_mobile:
            current_position = Gut.gut.positionOf[self]
            patches = Gut.gut.getNeighborhood(current_position)
            d = lambda patch:movement_cost if Gut.gut.positionOf[patch]!=current_position else 0
            destination = max(patches, key=lambda patch: patch.nutrient-d(patch))
            if Gut.gut.positionOf[destination] != current_position:
                Gut.gut.changePatch(self, destination)
                self.energy -= movement_cost
    
    def consume(self):
        (nutrient, TCA, DCA, toxin) = Gut.gut.getCompoundsAt(Gut.gut.positionOf[self])
        (nutrient, TCA, DCA, toxin) = self.processCompounds(nutrient, TCA, DCA, toxin)
        Gut.gut.putCompounds(Gut.gut.positionOf[self], nutrient, TCA, DCA, toxin)
        self.energy -= self.basal_metabolic_cost
    
    def checkHealth(self):
        if self.energy < 0:
            Gut.gut.removeAgent(self)
    
    def processCompounds(self, nutrient, TCA, DCA, toxin):
        '''
        Stub method; needs to be overridden by each subclass
        '''
        consumption = min(nutrient, 1)
        self.energy += consumption
        nutrient -= consumption
        return (nutrient, TCA, DCA, toxin)


    
class EpiCell(Cell): 
    
    basal_metabolic_cost = 0 
    
    def __init__(self, energy):
        super(EpiCell, self).__init__(energy)
    
    def checkHealth(self):
        if self.energy < (1-0.02):
            self.energy += 0.02
        if self.energy > 1.0:
            self.energy = 1
    
    def replicate(self):
        pass
    
    def processCompounds(self, nutrient, TCA, DCA, toxin):
        self.energy -= toxin
        nutrient += toxin
        toxin = 0
        if self.energy <0:
            self.energy = 0
        return (nutrient, TCA, DCA, toxin)


class Commensal(Cell):  
    basal_metabolic_cost = 0.5
    
    def __init__(self, energy):
        super(Commensal, self).__init__(energy)
    
    def processCompounds(self, nutrient, TCA, DCA, toxin):
        consumption = min(nutrient, 1)
        self.energy += consumption
        nutrient -= consumption
        TCAconsumed = random()*TCA
        DCA += TCAconsumed
        TCA -= TCAconsumed
        return (nutrient, TCA, DCA, toxin)
    

class Cdif_Spore(Cell):  
    
    basal_metabolic_cost = 0.1
    
    def __init__(self, energy):
        super(Cdif_Spore, self).__init__(energy)
        self.TCA = random()*cdif_germinate_threshold
    
    def processCompounds(self, nutrient, TCA, DCA, toxin):
        if self.energy < self.basal_metabolic_cost:
            consumption = min(nutrient, self.basal_metabolic_cost)
            self.energy += consumption
            nutrient -= consumption
        TCAconsumed = random()*TCA
        self.TCA += TCAconsumed
        TCA -= TCAconsumed
        return (nutrient, TCA, DCA, toxin)
    
    def replicate(self):
        if self.TCA > cdif_germinate_threshold and self.energy > cdif_sporulate_threshold:
            spawn = Cdif_Veg(self.energy)
            Gut.gut.spawn(spawn, Gut.gut.positionOf[self], neighbors=False)
            self.energy = -10
    

class Cdif_Veg(Cell):
    
    basal_metabolic_cost = 0.5  
    
    def __init__(self, energy):
        super(Cdif_Veg, self).__init__(energy)
        self.is_mobile = True
        self.DCA = 0
    
    def checkHealth(self):
        if self.energy < cdif_sporulate_threshold and self.energy>0:
            if random() < cdif_sporulate_chance:
                self.sporulate()
        elif self.DCA > cdif_sporulate_threshold and self.energy>0:
            self.sporulate()
        if self.energy < 0:
            pos = Gut.gut.positionOf[self]
            Gut.gut.removeAgent(self)
            
            
    def processCompounds(self, nutrient, TCA, DCA, toxin):
        consumption = min(nutrient, 1)
        self.energy += consumption
        nutrient -= consumption
        DCAconsumed = random()*DCA
        self.DCA += DCAconsumed
        DCA -= DCAconsumed
        toxin += toxin_production
        return (nutrient, TCA, DCA, toxin)
    
    def sporulate(self):
        spore = Cdif_Spore(self.energy)
        Gut.gut.spawn(spore, Gut.gut.positionOf[self], neighbors=False)
        self.energy = -10
    

            