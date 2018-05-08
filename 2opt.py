import numpy as np
from numpy import *
from random import *
import itertools


from itertools import permutations

# load the distnace matrix from file
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

def twoopt(route):
    j = 0
    tourLength = measurePath(route, distances)
    route = [cities[i] for i in route]
    print("iteration: {} tour: {} length: {}".format(j, route, tourLength))





maximalNoOfCities = 10

# load the distance matrix and city names
(cities, distances) = loadDistances()

# print city names
#print(cities[:maximalNoOfCities])

# print distance matrix
#print(distances[:maximalNoOfCities, :maximalNoOfCities])

# bruteforcen

route = np.random.permutation(maximalNoOfCities)
#route = [cities[i] for i in route]
#print(route)

twoopt(route)
