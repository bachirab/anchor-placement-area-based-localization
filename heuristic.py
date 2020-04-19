import argparse
import time
from our_library import *

shapely.speedups.enable()

parser = argparse.ArgumentParser()
parser.add_argument('--max_x', help='Give the MAX_X value', default=MAX_X, type=int)
parser.add_argument('--max_y', help='Give the MAX_Y value', default=MAX_Y, type=int)
parser.add_argument('--tics', help='Give the TICS value', default=TICS, type=int)
parser.add_argument('--nb_anchors', help='Give the number of anchors', default=NB_ANCHORS, type=int)

args = parser.parse_args()

max_x = args.max_x
max_y = args.max_y
tics = args.tics
nb_anchors = args.nb_anchors

print("tics=" + str(tics) + " anchors=" + str(nb_anchors))


# Param

def neighbor(point):
    """ Function return the neighbors of a point x in the matrix A
    take as input the coordinate of x and dim the dimension of A then
    returns the neighbors of x in the matrix B which have 2*dim elements.
    exemple:
    neighbor([2,1],4)
    returns : [[3, 1], [3, 2], [3, 3], [4, 1], [4, 2], [4, 3], [5, 1], [5, 2], [5, 3]]
    """
    a = np.array(point)
    epsilon = tics * 2
    adjacents = []
    for i in range(a[0] - epsilon, a[0] + epsilon + 1, tics):
        if 0 <= i < max_x - 1:
            for j in range(a[1] - epsilon, a[1] + epsilon + 1, tics):
                if 0 <= j < max_y - 1:
                    adjacents.append([i, j])
    return adjacents


# Param
minAvgRA = 999999999
positions = []
# For every number of anchors, we need to initialise the initial vector which gives the optimal
# anchor placement for the low discretisation.
initial = [(3255, 0), (3255, 9765), (9765, 6510)]  # 3 anchors 4*4
# Remember that [(3255, 0), (3255, 9765), (9765, 6510)] = [(7,0),(7,21),(21,14)]
# initial = [(6510, 3255), (6510, 9765), (9765, 0), (9765, 9765)] #4 anchors 4*4

results = []
# for choice in [7]:#,15,31]:
choice = 7
tics = 7 * 15 * tics // choice

optimal_anchors = []
anchors_list = []
neighbor_list = [neighbor(x) for x in initial]
for items in itertools.product(*neighbor_list):
    anchors_list.append(items)

start = time.time()
for index, nb_anchors in enumerate(tqdm(anchors_list)):
    l = getAllSubRegions(anchors_=nb_anchors, max_x_=max_x, max_y_=max_y)
    res = getDisjointSubRegions(l)
    avgRA = getExpectation(res)
    if avgRA != 0:
        if minAvgRA > avgRA:
            minAvgRA = avgRA
            optimal_anchors = []
            for a in nb_anchors:
                optimal_anchors.append(a)
            optimal_areas = res
end = time.time()

drawNetwork(optimal_anchors, optimal_areas, algo_="heuristic")

print("**Optimal Anchor Pos.:" + str(optimal_anchors), minAvgRA)
print('Runinig Times : ' + str(round((end - start) / 60.0, 2)) + ' (min.)')

f_res = open('./TXT/heuristic.txt', 'a')
f_res.write(str(optimal_anchors) + ';' + str(minAvgRA) + ';' + str(end - start) + ';' + str(NB_ANCHORS) + ';' + str(
    tics) + '\n')
f_res.close()

##TODO The initial point is from brute force, I find it by multiplying it with the TICS.
##TODO I should verify whether the results of the neigbhoor function is reduced to the current TICS
