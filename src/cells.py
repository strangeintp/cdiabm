'''
Created on Nov 28, 2017

@author: vince
'''

import Gut

''' Internal parameters'''
replication_threshold = 100  # TBD
movement_cost = 10 #TBD

gut = None

class Cell(object):
    '''
    This is a parent class for epithelial, commensal, and C dif cells
    '''


    def __init__(self, energy):
        '''
        Constructor
        '''
        self.energy = energy
        self.is_mobile = False   #Cdif_Veg overrides
        if gut==None:
            gut = Gut.gut
        
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
        self.energy -= self.basal_metabolic_cost
    
    def checkHealth(self):
        '''
        Cdif_Veg should override this method, with chance to sporulate
        Cdif_Spore should override this method, to convert to vegetative
        Epithelial cell class should override to put nutrient into environment (?)
        '''
        if self.energy < 0:
            gut.removeAgent(self)
    
    def processCompounds(self, nutrient, TCA, DCA, toxin):
        '''
        Stub method; needs to be overridden by each subclass
        '''
        return (nutrient, TCA, DCA, toxin)
    
class EpiCell(Cell):  
    
    def __init__(self, energy):
        super().__init__(energy)
    
    def processCompounds(self, nutrient, TCA, DCA, toxin):
            
            
            