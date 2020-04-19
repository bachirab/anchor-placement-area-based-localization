global NB_ANCHORS
# -*- coding: utf-8 -*-
"""Genetic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LAKWgnGOdLtdwpJJtZLdvNEeXuwQduq0
"""

import sys

from multiprocessing import Process, Queue, cpu_count
from sys import stdout
from random import random
import numpy as np
import time
from copy import deepcopy
import random
from our_library import *
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
#TICS = 7  # *15#*31


"""This next part is the Brute Force method

Genetic algorithm method
"""


class GA(object):
    """
        Implementation of a genetic algorithm
        for a permuation problem
    """

    def __init__(self, fitness_func,
                 n_individu=10,
                 gen=5,
                 dim=3,
                 CrossThreshold=0.9,
                 MutationThreshold=0.2,
                 MAX_X=4,
                 MAX_Y=4,
                 TICS=1):
        self.dim = dim * 2
        self.TICS = TICS
        self.space = MAX_X // TICS
        self.n_ind = n_individu
        self.gen = gen
        self.pop = []
        self.fitness_func = fitness_func
        self.all = []
        self.CrossThreshold = CrossThreshold
        self.MutationThreshold = MutationThreshold
        self.archive = []
        self.f_archive = []
        for i in range(MAX_X // TICS):
            for j in range(MAX_Y // TICS):
                self.all.append((i, j))
        for i in range(self.n_ind):
            self.pop.append(list(np.random.randint(0, self.space, self.dim) * TICS))

    def crossover(self, parents):
        first_parant, second_parent = parents
        index = np.random.randint(1, self.dim)
        child_1 = first_parant[:index] + second_parent[index:]
        child_2 = second_parent[:index] + first_parant[index:]
        return (child_1, child_2)

    def mutation(self, individual):
        #        new_place = np.random.choice(list( set(range(self.space)) - set(individual)))
        new_place = np.random.choice(range(self.space)) * self.TICS
        index = np.random.randint(0, self.dim)
        individual[index] = new_place
        return individual

    def selectParents(self, fitness_population):
        # Construct a iterator here
        # Use Tournament Selection
        while 1:
            parent1 = self.tournament(fitness_population)
            parent2 = self.tournament(fitness_population)
            yield (parent1, parent2)

    def tournament(self, fitness_population):
        fit1, ch1 = fitness_population[random.randint(0, len(fitness_population) - 1)]
        fit2, ch2 = fitness_population[random.randint(0, len(fitness_population) - 1)]
        return ch1 if fit1 < fit2 else ch2

    def fitness(self, individual):
        anchors = [individual[2 * i:2 * (i + 1)] for i in range(self.dim // 2)]
        unique = np.unique(anchors, axis=0)
        unique = [list(e) for e in unique]
        if len(unique) == len(anchors):
            f_ind = self.fitness_func(anchors)
            return f_ind[0]  # we just return the average
        else:
            return 99999999

    def eletism(self, rate, fitness_population):
        best = sorted([(x[0], fitness_population.index(x)) for x in fitness_population if x[0] is not None])[
               :int(rate * self.n_ind)]
        return [fitness_population[i[1]][1] for i in best]

    def update(self, fitness_population):
        #        allChildren = self.eletism(0.25, fitness_population)
        allChildren = []
        generator = self.selectParents(fitness_population)
        while len(allChildren) < len(fitness_population):
            parents = next(generator)
            if random.random() > self.CrossThreshold:
                children = self.crossover(parents)
            else:
                children = parents
            for child in children:
                if random.random() > self.MutationThreshold:
                    ch = self.mutation(child)
                    if ch not in self.archive:
                        allChildren.append(ch)
                else:
                    if child not in self.archive:
                        allChildren.append(child)
        # TODO Think about eletism
        return allChildren[:len(fitness_population)]  # May exceed

    def Work(self, anchors, q):
        f_ind = self.fitness(anchors)
        q.put(f_ind)

    def p_fitness(self, individuals):
        Result = []
        results = []
        cores = cpu_count()
        anchors_list = deepcopy(individuals)
        for index in range(len(anchors_list) // cores):
            q = Queue()
            P = []
            j = 0
            for i in range(cores):
                P.append(Process(target=self.Work, args=(anchors_list[index * cores + j], q)))
                j = j + 1
            for i in range(cores):
                P[i].start()

            for i in range(cores):
                results.append(q.get(True))

            for i in range(cores):
                P[i].join()
        i = 0
        for element in results:
            Result.append((element, individuals[i]))
            i += 1
        return Result

    def color(self, current, total):
        if current * 100 / total < 50:
            return "\033[91m %d \033[0m" % current
        if current * 100 / total < 75:
            return "\033[93m %d \033[0m" % current
        return "\033[92m %d \033[0m" % current


    def run(self):
        for i in np.arange(self.gen):
            stdout.write("\r%s/%d" % (self.color(i, self.gen), self.gen))
            stdout.flush()
            fitness_population = [(self.fitness(individual), individual) for individual in self.pop]
            self.f_archive = self.f_archive + fitness_population
            self.archive = self.archive + self.pop
            self.pop = self.update(fitness_population)

        self.f_archive.sort()
        for indice in self.f_archive:
            if indice[0] == None:
                pass
            else:
                optimal_ind = indice[1]
                break
        return [optimal_ind[2 * i:2 * (i + 1)] for i in range(self.dim // 2)]
        
        
    def decode(self,optimal_ind):
        return [optimal_ind[2 * i:2 * (i + 1)] for i in range(self.dim // 2)]


# ----------------------------


def Work(anchors):
    
    l = getAllSubRegions(anchors)
    #print(anchors)
    res = getDisjointSubRegions(l)
    avgRA = getExpectation(res)
    return [avgRA, res, anchors]


######### Main ()

if __name__ == "__main__":


    ga = GA(
        fitness_func=Work,
        n_individu=10,
        CrossThreshold=0.2,
        MutationThreshold=0.3,
        gen=20,
        dim=NB_ANCHORS,
        MAX_X=MAX_X,
        MAX_Y=MAX_Y,
        TICS=TICS
    )

    # with big space comes big responsabilty ( Mutation problem )

    start = time.time()
    optimal_anchors = ga.run()
    end = time.time()

    min_avg, residence_area_l, anchor = Work(optimal_anchors)

    drawNetwork(optimal_anchors, residence_area_l)
    print("\n**Optimal Anchor Position: ", optimal_anchors)
    print("**Minimum Avrg: " + str(min_avg))
    print('Runinig Times : ' + str(round((end - start) / 60.0, 2)) + ' (min.)')

    f_res = open('./IMG/ga.txt', 'a')
    f_res.write( str(optimal_anchors)+';' + str(min_avg)+';'+str(end - start)+';'+ str(NB_ANCHORS)+';'+str(TICS)+'\n')
    f_res.close()


