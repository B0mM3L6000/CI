import numpy as np
from numpy import *
from random import *
import itertools
import time


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


def bruteforce(maximalNoOfcities):
    shortestTourLength = sum(distances)
    j = 0

    #p = itertools.permutations(list(range(maximalNoOfCities)))
    for i in itertools.permutations(list(range(maximalNoOfCities))):
        j +=1

        # hier muss der bruteforce für die touren hin  und in variable p abspeichern

        # measure path length
        tourLength = measurePath(i, distances)

        # if new path is shorter than the old best path, remember the new path
        if tourLength < shortestTourLength:
            shortestTourLength = tourLength
            shortestTour = i

            # print the new shortest path
            shortestTourCities = [cities[i] for i in shortestTour]
            print("iteration: {} tour: {} length: {}".format(j, shortestTourCities, shortestTourLength))

        # do some status printing from time to time
        elif j % 100000 == 0:
            print('iteration: {}'.format(j))
    print(j)



# do not solve the 16 cities problem, as it is to large. try first with 6 cities
maximalNoOfCities = 10

# load the distance matrix and city names
(cities, distances) = loadDistances()

# print city names
#print(cities[:maximalNoOfCities])

# print distance matrix
#print(distances[:maximalNoOfCities, :maximalNoOfCities])

# bruteforcen
zeit1 = time.ctime()
bruteforce(maximalNoOfCities)
zeit2 = time.ctime()
print(zeit1)
print(zeit2)
