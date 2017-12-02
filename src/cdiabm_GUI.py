'''
Created on Dec 1, 2017

@author: vince
'''
import matplotlib
matplotlib.use('TkAgg')

import pylab as PL
import scipy as SP

import Gut
from Gut import grid_size, Initial_commensals, Initial_spores, Nutrient_replenish_rate, Antiobiotic_kill_rate
from random import random

cdict = {'red':   [(0.0, 0.35, 0.35),
                   (1.0, 0.5, 0.5)],
    
         'green': [(0.0, 0.35, 0.35),
                   (1.0, 0.2, 0.2)],
    
         'blue':  [(0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)]}
cmap = matplotlib.colors.LinearSegmentedColormap(name='R2Br', segmentdata=cdict, N=256)

dirNames = []

gui = None
plots = None
gut = None
counts = {}

def init():
    global envir, time, plots, gut, counts
    gut=Gut.Gut()
    time = 0
    plots = None
    counts = {}
    counts["health"] = [sum([cell.energy for cell in gut.epicells])/len(gut.epicells)]
    counts["commensals"] = [len(gut.commensals)]
    counts["cdif spores"] = [len(gut.cdif_spores)]
    counts["cdif germs"] = [len(gut.cdif_vegs)]
    
    
    envir = SP.zeros([grid_size, grid_size])
    for y in xrange(grid_size):
        for x in xrange(grid_size):
            envir[y, x] = 0
    
def draw():

    PL.cla()
    cmap.set_under()
    '''Plot Epicells as background'''
    PL.pcolormesh(gut.health(), cmap = cmap, vmin=0,vmax=1.0)
#     PL.pcolor(envir, cmap = PL.cm.YlOrRd, vmin = 0, vmax = 1)
    PL.axis('image')
    PL.hold(True)
    '''Plot Commensals'''
    cells = gut.commensals
    if cells:
        xyp = zip(*[gut.positionOf[cell] for cell in cells])
        jitter = 0.4
        x = [(0.5 + random()*jitter - jitter/2 + xp) for xp in list(xyp[0])]
        y = [(0.5 + random()*jitter - jitter/2 + yp) for yp in list(xyp[1])]
        s = [50 for cell in cells]
        PL.scatter(x, y, c = s, s=30, cmap = PL.cm.Blues, vmin = 0, vmax = 100)
    '''Plot Cdif spores'''
    cells = gut.cdif_spores
    if cells:
        xyp = zip(*[gut.positionOf[cell] for cell in cells])
        jitter = 0.4
        x = [(0.5 + random()*jitter - jitter/2 + xp) for xp in list(xyp[0])]
        y = [(0.5 + random()*jitter - jitter/2 + yp) for yp in list(xyp[1])]
        s = [0 for cell in cells]
        PL.scatter(x, y, c = s, s=30, cmap = PL.cm.binary, vmin = 0, vmax = 100)
    '''Plot Cdif vegs'''
    cells = gut.cdif_vegs
    if cells:
        xyp = zip(*[gut.positionOf[cell] for cell in cells])
        jitter = 0.4
        x = [(0.5 + random()*jitter - jitter/2 + xp) for xp in list(xyp[0])]
        y = [(0.5 + random()*jitter - jitter/2 + yp) for yp in list(xyp[1])]
        s = [50 for cell in cells]
        PL.scatter(x, y, c = s, s=30, cmap = PL.cm.Reds, vmin = 0, vmax = 100)
    PL.hold(False)
    PL.title('t = ' + str(time))
    drawPlots()

def drawPlots():
    global plots
    if plots == None or plots.canvas.manager.window == None:
        plots = PL.figure(2)
        PL.ion()
    PL.figure(2)
    PL.hold(True)
#     PL.cla()
    PL.subplot(4, 1, 1)    
    PL.plot(counts["health"], color = 'brown')
    PL.ylim(ymin=0, ymax=1.1)
    PL.title("Health")
    PL.subplot(4, 1, 2)
    PL.plot(counts["commensals"], color = 'blue')
    PL.ylim(ymin=0, ymax=max(counts["commensals"])*1.2)
    PL.title("commensals")
    PL.subplot(4, 1, 3)
    PL.plot(counts["cdif spores"], color = 'green')
    PL.ylim(ymin=0, ymax=max(counts["cdif spores"])*1.2)
    PL.title("C dif spores")
    PL.subplot(4, 1, 4)
    PL.plot(counts["cdif germs"], color = 'red')
    PL.ylim(ymin=0, ymax=max(1, max(counts["cdif germs"])*1.2))
    PL.title("C dif germs")
    plots.tight_layout()
    plots.canvas.manager.window.update()
    PL.figure(1)
    
def step():
    global time
    time += 1
    gut.step()
    computeMetrics()

def computeMetrics():
    global counts
    counts["health"].append(sum([cell.energy for cell in gut.epicells])/len(gut.epicells))
    counts["commensals"].append(len(gut.commensals))
    counts["cdif spores"].append(len(gut.cdif_spores))
    counts["cdif germs"].append(len(gut.cdif_vegs))

def run():
    global gui
    import pycxsimulator
    pSetters = [Initial_commensals,Initial_spores,Nutrient_replenish_rate, Antiobiotic_kill_rate]
    gui = pycxsimulator.GUI(parameterSetters=pSetters,stepSize=5)
    gui.start(func=[init,draw,step])

if __name__ == '__main__':
    run()


    