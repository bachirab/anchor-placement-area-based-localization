# -*- coding: utf-8 -*-
"""Brute Force.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WQOtFBJtH3RGjs-_INtIOfE4vv5LQ0gs
"""

from sys import stdout
from shapely.geometry import Point, MultiPolygon, Polygon
from random import random
from numpy import *
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import shapely.speedups
import sys
shapely.speedups.enable()
import argparse, sys
import time
from our_library import *
from shapely.wkt import loads, dumps

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

minAvgRA = 999999999

positions = []
for i in range(max_x // tics):
    for j in range(max_y // tics):
        positions.append((i * tics, j * tics))
anchors_list = list(combinations(positions, anchors))

start = time.time()
#anchors_list = [[(7, 0), (7, 21), (21, 7), (21, 14)]]
for index, anchors in enumerate(anchors_list):
 print(index,'/',len(anchors_list))
# stdout.write("\r%s/%d" % (color(index, len(anchors_list)), len(anchors_list)))
# stdout.flush()
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
# get the different residence area to draw them
end = time.time()
#drawNetwork(optimal_anchors, optimal_areas)
print("**Optimal Anchor Pos.:" + str(optimal_anchors), minAvgRA)
print('Runinig Times : ' + str(round((end - start) / 60.0, 2)) + ' (min.)')

f_res = open('./IMG/brute.txt', 'a')
f_res.write(str(optimal_anchors)+';'+str(minAvgRA)+';'+str(end - start)+';'+str(anchors)+';'+str(tics)+'\n')
f_res.close()
