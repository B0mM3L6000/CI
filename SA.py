import numpy as np
from numpy import *
from random import *
import random
import itertools


from itertools import permutations

# load the distance matrix from file
def loadDistances():
    distancesFile = open("citiesAndDistances.txt")
    cities = distancesFile.readline().split()
    del cities[16:]
    numCities = len(cities)
    cityDistances = zeros((numCities, numCities))
    for i in range(numCities):
        distances = distancesFile.readline().split()
        del distances[0]
        del distances[16:]
        for j in range(len(distances)):
            cityDistances[i, j] = int(distances[j])
    return (cities, cityDistances)


# compute for a permutation of citi names the trip length
def measurePath(p, distances):
    length = 0
    for i in range(len(p)):
        length += distances[p[i - 1], p[i]]
    return length


def kantentausch(p, k1, k2):
    #kanten vertauschen:
    #weg zwischen den kanten umdrehen
    pneu = np.copy(p)
    pneu[k1+1], pneu[k2] = pneu[k2], pneu[k1+1]
    pneu[k1+2:k2] = pneu[k2-1:k1+1:-1]

    pneu = array(pneu)
    return pneu

def node_insert(p, node, kante):
    pneu = np.copy(p)
    temp = pneu[node]
    print(temp)
    if kante < node:
        pneu[kante+2:node+1] = pneu[kante+1:node]
        pneu[kante+1] = temp
    else:
        pneu[node:kante] = pneu[node+1:kante+1]
        pneu[kante] = temp
    pneu = array(pneu)
    return pneu

def node_exchange(p, node1, node2):
    pneu = np.copy(p)
    pneu[node1], pneu[node2] = pneu[node2], pneu[node1]
    return pneu

"""

def twoopt_random(p, maxepisodes):
    #auswaehlen von 2 kanten (dargestellt jeweils durch den index des ersten knoten der kante)
    j = 0
    tourLength = measurePath(p, distances)
    route = [cities[i] for i in p]
    print("iteration: {} tour: {} length: {}".format(j, route, tourLength))
    for j in range(maxepisodes):
        k1 = random.randint(0, len(p)-3)
        k2 = random.randint(k1+2, len(p)-1)
        pneu = kantentausch(p,k1,k2)
        tourLengthNeu = measurePath(pneu, distances)
        if tourLengthNeu < tourLength:
            p = pneu
            tourLength = tourLengthNeu
            route = [cities[i] for i in p]
            print("iteration: {} tour: {} length: {}".format(j+1, route, tourLength))
        elif j%100000 == 0:
            print("Episode:", j)
    print("Best tour: {} length: {}".format(route, tourLength))

"""

"""
def cool1(temperatur, t):
    #abkühlen der temperatur T
    return newtemperature
"""

"""
def cool2(temperatur, t):
    #abkühlen der temperatur T
    return newtemperature
"""

"""
def cool3(temperatur, t):
    #abkühlen der temperatur T
    return newtemperature
"""



def SA(p, maxepisodes,cooling):
    t = 1
    temperature = 1
    for j in range(maxepisodes):
        randomoperator = randint(1,3)
        if randomoperator == 1:
            #mache kantentausch
            k1 = random.randint(0, len(p) - 3)
            k2 = random.randint(k1 + 2, len(p) - 1)
            pneu = kantentausch(p, k1, k2)
        elif randomoperator == 2:
            #mache node insert
            node = randint(0, len(p)-1)
            kante = choice([i for i in range(0, len(p)-1) if i not in [node, node-1]])
            pneu = node_insert(node, kante)
        elif randomoperator == 3:
            #mache node exchange
            node1 = randint(0, len(p)-3)
            node2 = randint(node1+2, len(p)-1)
            pneu = node_exchange(node1, node2)

        epsilon = random.rand(0,1)

        fneu = measurePath(pneu, distances)
        falt = measurePath(p, distances)

        if epsilon <= (e**((fneu - falt)/temperature)):
            #update neue tour
            p = pneu
            route = [cities[i] for i in p]
            print("iteration: {} tour: {} length: {}".format(j+1, route, fneu))
        elif fneu <= falt:
            #update neue tour
            p = pneu
            route = [cities[i] for i in p]
            print("iteration: {} tour: {} length: {}".format(j+1, route, fneu))
        elif (j+1)%100000 == 0:
            print("Episode:", j+1)

        if cooling == 1:
            temperature = cool1(temperature, t)
        elif cooling == 2:
            temperature = cool2(temperature, t)
        elif cooling == 3:
            temperature = cool1(temperature, t)
            
        t +=1


maximalNoOfCities = 10

# load the distance matrix and city names
(cities, distances) = loadDistances()

# print city names
#print(cities[:maximalNoOfCities])

# print distance matrix
#print(distances[:maximalNoOfCities, :maximalNoOfCities])

maxepisodes = 1000000
#p = np.random.permutation(maximalNoOfCities)    #initialisieren einer zufälligen route zum starten
#route = [cities[i] for i in p]    #zuordnen der namen zu den indexen
#print(route)   #ausgabe der route mit namen
testarray = array([1,2,3,4,5,6,7,8,9,10])
#print(p)    #ausgabe der route mit indexn

#twoopt_random(p, maxepisodes)
test = node_insert(testarray, 2, 7)
print(testarray)
print(test)