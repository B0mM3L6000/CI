import numpy as np
from numpy import *
from random import *
import random
import itertools
import math
import time


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
    #print(temp)
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



#linear:
def cool1(starttemperatur,endtemperature, t, maxepisodes):
    #abkühlen der temperatur T
    newtemperature = starttemperatur - t*(starttemperatur-endtemperature)/maxepisodes
    return newtemperature



def cool2(starttemperatur,endtemperature, t, maxepisodes):
    #abkühlen der temperatur T
    newtemperature = starttemperatur*((endtemperature/starttemperatur)**(t/maxepisodes))
    return newtemperature



def cool3(starttemperatur,endtemperature, t, maxepisodes):
    #abkühlen der temperatur T
    newtemperature = starttemperatur * (2.718 ** ((-1)*(1/(maxepisodes**2))*math.log(starttemperatur/endtemperature)*(t**2)))
    return newtemperature




def SA(p, maxepisodes,cooling):
    t = 1
    temperature = 1
    starttemperature = 1
    endtemperature = 0.00001
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
            pneu = node_insert(p, node, kante)
        elif randomoperator == 3:
            #mache node exchange
            node1 = randint(0, len(p)-3)
            node2 = randint(node1+2, len(p)-1)
            pneu = node_exchange(p, node1, node2)

        epsilon = random.uniform(0,1)

        fneu = measurePath(pneu, distances)
        falt = measurePath(p, distances)

        if epsilon <= (2.718**(((fneu - falt)/temperature)*(-1))):
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

        #print(temperature)

        if cooling == 1:
            temperature = cool1(starttemperature, endtemperature, t, maxepisodes)
        elif cooling == 2:
           temperature = cool2(starttemperature, endtemperature, t, maxepisodes)
        elif cooling == 3:
            temperature = cool1(starttemperature, endtemperature, t, maxepisodes)

        t +=1
    return p




# load the distance matrix and city names
(cities, distances) = loadDistances()

# print city names
#print(cities[:maximalNoOfCities])

# print distance matrix
#print(distances[:maximalNoOfCities, :maximalNoOfCities])

#hyperparameter:
maxepisodes = 1000000
coolingschema = 3
maximalNoOfCities = 10

#p = np.random.permutation(maximalNoOfCities)    #initialisieren einer zufälligen route zum starten

#route = [cities[i] for i in p]    #zuordnen der namen zu den indexen
#print(route)   #ausgabe der route mit namen
#testarray = array([1,2,3,4,5,6,7,8,9,10])
#print(p)    #ausgabe der route mit indexn

#twoopt_random(p, maxepisodes)

#zeit1 = time.time()
#zeit1 = time.ctime()
#SA(p, maxepisodes, coolingschema)
#zeit2 = time.ctime()
#zeit2 = time.time()
#print(zeit2-zeit1)
#print(time)
#print(time2)
#print(time2-time)


#daten für aufgabe erheben:
dauern = list()
routen = list()
laengen = list()

for coolingvariable in range(1,4):
    for durchlaufe in range(5):
        zeit1 = time.time()
        p = np.random.permutation(maximalNoOfCities)
        p = SA(p, maxepisodes, coolingvariable)
        plength = measurePath(p, distances)
        zeit2 = time.time()
        dauer = zeit2 - zeit1
        dauern.append(dauer)
        routen.append(p)
        laengen.append(plength)

print("Coolingschema 1:")
mittellaenge = 0
mittelzeit = 0
beste = 0
for i in range(5):
    print("Routenlaenge:", laengen[i],"Zeit:",dauern[i], "Sekunden")
    mittellaenge += laengen[i]
    mittelzeit += dauern[i]
    if laengen[i] > beste:
        beste = laengen[i]
print("Mittelwert Laenge:", (mittellaenge/5), "Mittelwert Zeit:", (mittelzeit/5), "Beste Tourenlaenge:", beste)
print("Coolingschema 2:")
mittellaenge = 0
mittelzeit = 0
beste = 0
for i in range(5):
    print("Routenlaenge:", laengen[i+5],"Zeit:",dauern[i+5], "Sekunden")
    mittellaenge += laengen[i+5]
    mittelzeit += dauern[i+5]
    if laengen[i+5] > beste:
        beste = laengen[i+5]
print("Mittelwert Laenge:", (mittellaenge/5), "Mittelwert Zeit:", (mittelzeit/5), "Beste Tourenlaenge:", beste)
mittellaenge = 0
mittelzeit = 0
beste = 0
print("Coolingschema 3:")
for i in range(5):
    print("Routenlaenge:", laengen[i+10],"Zeit:",dauern[i+10], "Sekunden")
    mittellaenge += laengen[i+10]
    mittelzeit += dauern[i+10]
    if laengen[i+10] > beste:
        beste = laengen[i+10]
print("Mittelwert Laenge:", (mittellaenge/5), "Mittelwert Zeit:", (mittelzeit/5), "Beste Tourenlaenge:", beste)
