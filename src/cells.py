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
            destination = max(patches, key=lambda patch: patch.nutrient)
            if Gut.gut.positionOf[destination] != current_position:
                Gut.gut.changePatch(self, destination)
                self.energy -= movement_cost
    
    def consume(self):
        (nutrient, TCA, DCA, toxin) = Gut.gut.getCompoundsAt(Gut.gut.positionOf[self])
        (nutrient, TCA, DCA, toxin) = self.processCompounds(nutrient, TCA, DCA, toxin)
        Gut.gut.putCompounds(Gut.gut.positionOf[self], nutrient, TCA, DCA, toxin)
        self.energy -= self.basal_metabolic_cost
    
    def checkHealth(self):
        '''
        '''
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
    
    def replicate(self):
        pass
    
    def processCompounds(self, nutrient, TCA, DCA, toxin):
        consumption = 0
        self.energy += consumption
        nutrient -= consumption
        self.energy -= toxin
        toxin = 0
        return (nutrient, TCA, DCA, toxin)


class Commensal(Cell):  
    basal_metabolic_cost = 0.5
    
    def __init__(self, energy):
        super(Commensal, self).__init__(energy)
    
    def processCompounds(self, nutrient, TCA, DCA, toxin):
        consumption = min(nutrient, 1)
        self.energy += consumption
        nutrient -= consumption
        TCAconsumed = min(TCA, 5*cdif_germinate_threshold)
        DCA += TCAconsumed
        TCA -= TCAconsumed
        return (nutrient, TCA, DCA, toxin)
    

class Cdif_Spore(Cell):  
    
    basal_metabolic_cost = 0.5
    
    def __init__(self, energy):
        super(Cdif_Spore, self).__init__(energy)
        self.TCA = 0
    
    def processCompounds(self, nutrient, TCA, DCA, toxin):
        consumption = min(nutrient, 1)
        self.energy += consumption
        nutrient -= consumption
        TCAconsumed = min(TCA, cdif_germinate_threshold)
        self.TCA += TCAconsumed
        TCA -= TCAconsumed
        return (nutrient, TCA, DCA, toxin)
    
    def replicate(self):
        if self.energy > replication_threshold and self.TCA > cdif_germinate_threshold:
            #TBD is there energy expenditure in replication?
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
        if self.energy < cdif_sporulate_threshold:
            if random() < cdif_sporulate_chance:
                self.sporulate()
            elif self.energy < 0:
                pos = Gut.gut.positionOf[self]
                Gut.gut.putCompounds(pos, death_nutrients, 0, 0, 0)
                Gut.gut.removeAgent(self)
        elif self.DCA > cdif_sporulate_threshold:
            spore = Cdif_Spore(self.energy)
            Gut.gut.spawn(spore, Gut.gut.positionOf[self], neighbors=False)
            Gut.gut.removeAgent(self)
            
            
    def processCompounds(self, nutrient, TCA, DCA, toxin):
        consumption = min(nutrient, 1)
        self.energy += consumption
        nutrient -= consumption
        DCAconsumed = min(DCA, cdif_sporulate_threshold)
        self.DCA += DCAconsumed
        DCA -= DCAconsumed
        toxin += toxin_production
        return (nutrient, TCA, DCA, toxin)
    
    def sporulate(self):
        spore = Cdif_Spore(self.energy)
        Gut.gut.spawn(spore, Gut.gut.positionOf[self], neighbors=False)
        self.energy = -10
    

            