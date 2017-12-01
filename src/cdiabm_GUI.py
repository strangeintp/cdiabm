'''
Created on Dec 1, 2017

@author: vince
'''
import matplotlib
matplotlib.use('TkAgg')

import pylab as PL
import scipy as SP

import Gut
from Gut import grid_size
from random import random

cdict = {'red':   [(0.0,  0.0, 0.0),
                   (1.0,  0.0, 0.0)],
    
         'green': [(0.0,  0.0, 0.0),
                   (1.0,  1.0, 1.0)],
    
         'blue':  [(0.0,  0.0, 0.0),
                   (1.0,  0.0, 0.0)]}
cmap = matplotlib.colors.LinearSegmentedColormap(name='G', segmentdata=cdict, N=256)

dirNames = []

def init():
    global envir, time
    Gut.Gut()
    time = 0
    
    envir = SP.zeros([grid_size, grid_size])
    for y in xrange(grid_size):
        for x in xrange(grid_size):
            envir[y, x] = 0
    
def draw():
    '''
    PL.cla()
    cmap.set_under()
    PL.pcolormesh(epicell_healths, cmap = cmap, vmin=0,vmax=max_health)
    PL.axis('scaled')
    PL.hold(True)
    xyp = zip(*[theWorld.hh_locations[hh] for hh in theWorld.households])
    xy = [list(t) for t in xyp]
    
    if len(xy)>0:
        x = [i+0.5 for i in xy[0]]
        y = [i+0.5 for i in xy[1]]
        lineage = [hh.lineage for hh in (theWorld.households)]
        hh_size = [20*hh.size() for hh in (theWorld.households)]
        PL.scatter(y, x, c = lineage, s=hh_size, vmin=0, vmax=W.starting_agents, cmap = plt.get_cmap('hsv'))
        message = r't = {0}     Pop.: {1}     HHs: {2}    max HHs: {3}'
        PL.title(message.format(time, theWorld.population, len(theWorld.households), max(lineage))) 
    PL.hold(False)
    figure.tight_layout()
    '''
    PL.cla()
    PL.pcolor(envir, cmap = PL.cm.YlOrRd, vmin = 0, vmax = 1)
    PL.axis('image')
    PL.hold(True)
    '''Plot Epicells'''
    cells = Gut.gut.epicells
    if cells:
        xyp = zip(*[Gut.gut.positionOf[cell] for cell in cells])
        jitter = 0.2
        x = [(0.5 + random()*jitter - jitter/2 + xp) for xp in list(xyp[0])]
        y = [(0.5 + random()*jitter - jitter/2 + yp) for yp in list(xyp[1])]
        s = [50 for cell in cells]
        PL.scatter(x, y, c = s, s=75, cmap = PL.cm.RdPu, vmin = 0, vmax = 100)
    '''Plot Commensals'''
    cells = Gut.gut.commensals
    if cells:
        xyp = zip(*[Gut.gut.positionOf[cell] for cell in cells])
        jitter = 0.4
        x = [(0.5 + random()*jitter - jitter/2 + xp) for xp in list(xyp[0])]
        y = [(0.5 + random()*jitter - jitter/2 + yp) for yp in list(xyp[1])]
        s = [50 for cell in cells]
        PL.scatter(x, y, c = s, s=30, cmap = PL.cm.Blues, vmin = 0, vmax = 100)
    '''Plot Cdif spores'''
    cells = Gut.gut.cdif_spores
    if cells:
        xyp = zip(*[Gut.gut.positionOf[cell] for cell in cells])
        jitter = 0.4
        x = [(0.5 + random()*jitter - jitter/2 + xp) for xp in list(xyp[0])]
        y = [(0.5 + random()*jitter - jitter/2 + yp) for yp in list(xyp[1])]
        s = [0 for cell in cells]
        PL.scatter(x, y, c = s, s=30, cmap = PL.cm.binary, vmin = 0, vmax = 100)
    '''Plot Cdif vegs'''
    cells = Gut.gut.cdif_vegs
    if cells:
        xyp = zip(*[Gut.gut.positionOf[cell] for cell in cells])
        jitter = 0.4
        x = [(0.5 + random()*jitter - jitter/2 + xp) for xp in list(xyp[0])]
        y = [(0.5 + random()*jitter - jitter/2 + yp) for yp in list(xyp[1])]
        s = [1 for cell in cells]
        PL.scatter(x, y, c = s, s=30, cmap = PL.cm.binary, vmin = 0, vmax = 100)
    PL.hold(False)
    PL.title('t = ' + str(time))
    
def step():
    global time
    time += 1
    Gut.gut.step()

def run():
    import pycxsimulator
    pycxsimulator.GUI().start(func=[init,draw,step])

if __name__ == '__main__':
    run()


    