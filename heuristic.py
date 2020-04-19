from sys import stdout
from copy import deepcopy
from shapely.geometry import Point, MultiPolygon, Polygon
from random import random
from numpy import *
import numpy as np
from itertools import combinations
import itertools
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import shapely.speedups
import sys

shapely.speedups.enable()
import time
from our_library import *
from shapely.wkt import loads, dumps
import argparse, sys

parser=argparse.ArgumentParser()
parser.add_argument('--max_x', help='Give the MAX_X value', default=MAX_X)
parser.add_argument('--max_y', help='Give the MAX_Y value', default=MAX_Y)
parser.add_argument('--tics', help='Give the TICS value', default=TICS)
parser.add_argument('--anchors', help='Give the number of anchors', default=NB_ANCHORS)

args=parser.parse_args()

max_x = args.max_x
max_y = args.max_y
tics = args.tics
anchors = args.anchors

print("tics=" + str(tics) + " anchors=" + str(anchors))

# Param


def neighboor(point):
    """ Function return the neighboors of a point x in the matrix A
    take as input the coordinate of x and dim the dimension of A then
    returns the neighboors of x in the matrix B which have 2*dim elements.
    exemple:
    neighboor([2,1],4)
    returns : [[3, 1], [3, 2], [3, 3], [4, 1], [4, 2], [4, 3], [5, 1], [5, 2], [5, 3]]
    """
    a = np.array(point)
    epsilon = tics*2
    adjacents = []
    for i in range(a[0]-epsilon,a[0]+epsilon+1,tics):
        if i>=0 and i<MAX_X-1:
            for j in range(a[1]-epsilon,a[1]+epsilon+1,tics):
                if j>=0 and j<MAX_X-1:
                    adjacents.append([i,j])
    return adjacents


# Param
NB_ANCHORS = 3 #<---- please change this wen updating the number of anchors
inAvgRA = 999999999
positions = []
dictionnaire = []
indice = 0
duration = 0


# For every number of anchors, we need to initialise the initial vector which gives the optimal
# anchor placement for the low discretisation.
initial = [(3255, 0), (3255, 9765), (9765, 6510)]    #3 anchors 4*4
# Remember that [(3255, 0), (3255, 9765), (9765, 6510)] = [(7,0),(7,21),(21,14)]
#initial = [(6510, 3255), (6510, 9765), (9765, 0), (9765, 9765)] #4 anchors 4*4
##### [(7, 14), (14, 7), (21, 21)] 3 anchors 4*4
results = []
print(neighboor([7,7],15*31))

#for choice in [7]:#,15,31]:
choice = 7
start = time.time()
tics = 7*15*tics // choice
optimal_anchors = []
anchors_list = []
listneighboors = [neighboor(x) for x in initial]
print(len(listneighboors))
for items in itertools.product(*listneighboors):
    anchors_list.append(items)
print(len(anchors_list))
for index,anchors in enumerate(anchors_list):
    stdout.write("\r%s/%d" % (color(index,len(anchors_list)), len(anchors_list)) )
    stdout.flush()
    l = getAllSubRegions(anchors,max_x,max_y)
    res = getDisjointSubRegions(l)
    avgRA = getExpectation(res)
    if avgRA != 0:
        if minAvgRA > avgRA:
            minAvgRA = avgRA
            optimal_anchors = []
        for a in anchors:
            optimal_anchors.append(a)
        optimal_areas = res
end = time.time()

duration = end - start

print("**Optimal Anchor Pos.:"+str(optimal_anchors), minAvgRA)
print('Runinig Times : '+str(round((end - start) / 60.0, 2)) +' (min.)')

fres = open('nb.txt','a')
for line in results:
    fres.write(line+'\n')

f_res = open('./IMG/heuristic.txt', 'a')
f_res.write(str(optimal_anchors)+';'+str(minAvgRA)+';'+str(end - start)+';'+str(NB_ANCHORS)+';'+str(tics)+'\n')
f_res.close()

##TODO The initial point is from brute force, I find it by multiplying it with the TICS.
##TODO I should verify whether the results of the neigbhoor function is reduced to the current TICS
