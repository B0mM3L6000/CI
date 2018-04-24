import numpy as np
from numpy import *
from random import *
from itertools import permutations

# load the distnace matrix from file
def loadDistances():
	distancesFile = open("citiesAndDistances.txt")
	cities = distancesFile.readline().split()
	del cities[16:]
	numCities = len(cities)
	cityDistances = zeros((numCities,numCities))
	for i in range(numCities):
		distances = distancesFile.readline().split()
		del distances[0]
		del distances[16:]
		for j in range(len(distances)):
			cityDistances[i,j] = int(distances[j])
	return (cities,cityDistances)

# compute for a permutation of citi names the trip length
def measurePath(p, distances):
	length = 0
	for i in range(len(p)):
		length += distances[p[i-1],p[i]]
	return length