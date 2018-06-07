from collections import deque
from city import distance, GeoCity, Euc_2D, GeoCoord
from tspparse import read_tsp_file
from numpy import array
import time
import numpy as np
import random
import sys

def calc_distance(tsp, city1_index, city2_index):
    """Calculate distance between cities by their (one-based) indices"""
    cities = tsp["CITIES"]
    return distance(cities[city1_index - 1], cities[city2_index - 1])


def path_length(tsp, path):
    """Find the length of a path of cities given as a list"""
    if len(path) == 1:
        return 0
    else:
        start_node = path.pop()
        next_node = path[-1]
        return calc_distance(tsp, start_node, next_node) + path_length(tsp, path)


def tour_from_path(path):
    """Append the first city in a path to the end in order to obtain a tour"""
    path.append(path[0])
    return path


def in_order_path(tsp):
    """Return the tour [1,2,...,n,1] where n is the dimension of the TSP"""
    dim = tsp["DIMENSION"]
    return list(range(1, dim + 1))


def in_order_tour(tsp):
    """Return the tour obtained by traveling to each city in order and
circling around back to the first city"""
    return tour_from_path(in_order_path(tsp))


def calc_in_order_tour(tsp):
    """Calculate the distance of the in-order-tour for a tsp"""
    return path_length(tsp, in_order_tour(tsp))


def nearest_neighbor(tsp, untraveled_cities, current_city):
    """Given a set of city keys, find the key corresponding to the
closest city"""
    distance_to_current_city = lambda city: calc_distance(tsp, current_city, city)
    return min(untraveled_cities, key=distance_to_current_city)


def furthest_neighbor(tsp, untraveled_cities, current_city):
    """Given a set of city keys, find the key corresponding to the
closest city"""
    distance_to_current_city = lambda city: calc_distance(tsp, current_city, city)
    return max(untraveled_cities, key=distance_to_current_city)


def nearest_neighbor_tour(tsp):
    """Construct a tour through all cities in a TSP by following the nearest
neighbor heuristic"""
    nearest_neighbor_path = [1]
    current_city = 1
    cities_to_travel = set(range(2, tsp["DIMENSION"] + 1))

    while cities_to_travel:
        current_city = nearest_neighbor(tsp, cities_to_travel, current_city)
        nearest_neighbor_path.append(current_city)
        cities_to_travel.remove(current_city)

    return tour_from_path(nearest_neighbor_path)


def furthest_neighbor_tour(tsp):
    """Construct a tour through all cities in a TSP by following the furthest
neighbor heuristic"""
    nearest_neighbor_path = [1]
    current_city = 1
    cities_to_travel = set(range(2, tsp["DIMENSION"] + 1))

    while cities_to_travel:
        current_city = furthest_neighbor(tsp, cities_to_travel, current_city)
        nearest_neighbor_path.append(current_city)
        cities_to_travel.remove(current_city)

    return tour_from_path(nearest_neighbor_path)


def calc_nearest_neighbor_tour(tsp):
    return path_length(tsp, nearest_neighbor_tour(tsp))


def calc_furthest_neighbor_tour(tsp):
    return path_length(tsp, furthest_neighbor_tour(tsp))


def node_xchg_step(tour):
    ## exchange nodes in a tour
    # i and k should be between ZERO and #CITIES-1
    # print 'node exchange', tour, i, k
    i = random.randint(0, len(tour) - 1)
    k = random.randint(0, len(tour) - 1)
    node = tour[i]
    tour[i] = tour[k]
    tour[k] = node
    return tour


# implementation of a hill climber
def HC_tour(tsp, max_iterations):
    start_time = time.time()
    tour = [i for i in range(tsp["DIMENSION"] + 1)]
    random.shuffle(tour)
    tour_len = path_length(tsp, tour_from_path(list(tour)))
    visited_tours = 1

    # best solution found so far
    best_tour = tour
    best_tour_len = tour_len

    # iterate max_iterations times
    while visited_tours < max_iterations:
        # derive a new tour
        new_tour = node_xchg_step(list(tour))
        new_tour_len = path_length(tsp, tour_from_path(list(new_tour)))
        visited_tours += 1

        # found a better one?
        if new_tour_len < tour_len:
            print('improved from', tour_len, 'to', new_tour_len, 'by', tour_len - new_tour_len, 'visited tours',
                  visited_tours)
            tour = new_tour
            tour_len = new_tour_len

    time_consumed = time.time() - start_time
    print('time consumed', time_consumed, 'tours visited', visited_tours, 'number of tours per second',
          visited_tours / time_consumed)
    return (best_tour)


def calc_HC_tour(tsp):
    return path_length(tsp, HC_tour(tsp, 100000))

"""
def node_xchg_step(tour):
    ## exchange nodes in a tour
    # i and k should be between ZERO and #CITIES-1
    # print 'node exchange', tour, i, k
    i = random.randint(0, len(tour) - 1)
    k = random.randint(0, len(tour) - 1)
    node = tour[i]
    tour[i] = tour[k]
    tour[k] = node
    return tour
"""
#mutation 1:
def pairswap(tour, p = 0.4):
    #mache einen pairswap mit wahrscheinlichkeit p
    randomnumber = random.uniform(0,1)
    newtour = tour
    if randomnumber <= p:
        gene1 = random.randint(0,len(tour)-1)   #auswählen der 2 gene
        gene2 = random.randint(0,len(tour)-1)
        while gene2 == gene1:
            gene2 = random.randint(0,len(tour)-1)
        newtour[gene1], newtour[gene2] = newtour[gene2], newtour[gene1]   #tauschen der gene
    return newtour

#mutation 2:
def arbper(tour, p = 0.4):
    #mache eine arbitrary permutation mit wahrscheinlichkeit p
    randomnumber = random.uniform(0,1)
    newtour = tour
    if randomnumber <= p: #auswählen der grenzen für die arb permutation
        bound1 = random.randint(0,len(tour)-1)
        bound2 = random.randint(0,len(tour)-1)
        while bound2 == bound1:
            bound2 = random.randint(0,len(tour)-1)
        if bound2 < bound1: #sortieren
            bound2, bound1 = bound1, bound2
        bound2 += 1 #wichtig für indexe
        tmptour = newtour[bound1:bound2]    #ab hier durchführen der veränderung
        tmptour = random.sample(tmptour, len(tmptour)) #(sufflen)
        for _ in range(bound1,bound2): #geshuffeltes element wieder einfügen und vorher altes entfernen
            newtour.pop(bound1)
        for i in range(bound1, bound2):
            newtour.insert(i, tmptour[i-bound1])
    return newtour    #neue tour ausgeben


# crossover 1:
# uniform order-based crossover:

def uobcrossover(parent1, parent2, p = 0.4):
    newtour = parent1
    gaps = [0 for i in range(len(newtour))] #erstelle liste für gaps
    for i in range(len(newtour)):   #mit wahrscheinlichkeit p wird ein gap gemacht (kodiert durch 1 in gaps)
        randomnumber = random.uniform(0,1)
        if randomnumber <= p:
            gaps[i] = 1
    genes1 = []
    for i in range(len(newtour)):   #auslesen welche werte die gaps im parent 1 haben
        if gaps[i] == 1:
            genes1.append(parent1[i])
    genes2 = []
    for i in range(len(parent2)):   #auslesen welche reihenfolge sie in partent2 haben
        tmp = parent2[i]
        if tmp in genes1:
            genes2.append(parent2[i])
    for i in range(len(newtour)):   #crossoverschritt
        if gaps[i] == 1:
            newtour[i] = genes2[j]
            j += 1
    return newtour


# crossover 2:
# edge recombination:

def edge_recomb(parent1, parent2, p = 0.4):
    newtour = []
    table = [[] for i in range(len(parent1))]  #2dimensionale liste
    # edge table erstellen:
    tmp1 = parent1[0] - 1
    tmp2 = parent2[0] - 1
    table[tmp1].append(parent1[len(parent1)-1])
    table[tmp1].append(parent1[1])
    table[tmp2].append(parent2[len(parent2)-1])
    table[tmp2].append(parent2[1])
    for i in range(1, len(parent1)-1):
        tmp1 = parent1[i] - 1
        tmp2 = parent2[i] - 1
        table[tmp1].append(parent1[i-1])
        table[tmp1].append(parent1[i+1])
        table[tmp2].append(parent2[i-1])
        table[tmp2].append(parent2[i+1])
    tmp1 = parent1[len(parent1)-1] - 1
    tmp2 = parent2[len(parent1)-1] - 1
    table[tmp1].append(parent1[len(parent1)-2])
    table[tmp1].append(parent1[0])
    table[tmp2].append(parent2[len(parent2)-2])
    table[tmp2].append(parent2[0])
    print(table)
    #doppelte einträge markieren und auf eine zahl reduzieren:

    #erstellen des kindes:
    #auswahl des ersten allels von parent1:
    tmp = parent1[0]-1
    for i in range(len(parent1)):
        newtour.append(tmp+1)
        #löschen dieses allels aus dem edge table:
        #auswahl neues allel anhand regeln
        tmp = #neues allel

    return newtour





# implements n tournament selection
def tournament_selection(fitness, n):
    if n < 1:   #error falls n kleiner 1 da nur mit 1 odermehr funktioniert
        sys.exit("ERROR in n tournament selection: n is smaller than 1")

    index = random.randint(0, len(fitness) - 1) #auswählen des ersten kandidaten zufällig
    n = n - 1 #verringern damit nur n kandidaten ausgewhählt werden

    while n > 0: #solange ausführen bis n kandidaten am turnier teilgenommen haben
        index2 = random.randint(0, len(fitness) - 1) #'contester' für beste fitness gegenüber bisherigem
        n = n - 1 #verringern damit nur n kandidaten ausgewhählt werden
        if fitness[index2] < fitness[index]: #wenn neuer kandidat besser (kürzere tour) ist dann ersetzten
            index = index2

    return index   #ausgeben des besten Kandidaten des Turniers

def recombine(a,b):
    return a


# implementation of an Evolutionary Algorithm
def EA_tour(tsp, population_size, max_generations):
    start_time = time.time()   #initialisieren der zeit zur bewertung

    # generate population
    # evaluate population and find best individual
    print("0010: generating initial population")
    pop = []
    fit = []
    for j in range(0, population_size):
        pop.append([i for i in range(tsp["DIMENSION"])])
        random.shuffle(pop[-1])
        fit.append(path_length(tsp, tour_from_path(list(pop[-1]))))

    # do max_generations iterations
    print("0020: starting the generations loop")
    for gen in range(0, max_generations):
        print("0022: Generation:", gen)

        # pop1=select parents
        print("0030: selecting parents via tournament selection")
        parents1 = []
        parents2 = []
        for _ in range(0, population_size):
            parents1.append(list(pop[tournament_selection(fit, 3)])) #auswählen eines elternpaars
            parents2.append(list(pop[tournament_selection(fit, 3)])) #aus der population mit dem index aus tourney select

        # pop2=recombine
        print("0040: recombining parents")
        children = [] #kinder initialisieren
        for i in range(0, population_size):
            #children.append(recombine(parents1[i], parents2[i])) #elternpaare kombinieren um kinder zu erstellen
            children.append(uobcrossover(parents1[i], parents2[i])) # uniform order based crossover (default p = 0.4)

        # pop3=mutate (arbper oder pairswap / gegebenfalls noch wahrscheinlichkeit
        #              anpassen mit parameter p [default auf 0.4])
        print("0050: mutating children")
        for i in range(0, population_size):
            arbper(children[i]) #kinder mutieren
            #pairswap(children[i])

        # evaluate pop3
        print("0060: evaluating fitness of the children")
        fit_children = []
        for j in range(0, population_size):
            fit_children.append(path_length(tsp, tour_from_path(list(children[j]))))

        # pop = select new parents from pop3
        print("0070: selecting new parents")
        pop = pop + children
        fit = fit + fit_children
        fit, pop = zip(*sorted(zip(fit, pop)))
        pop = list(pop[0:population_size])
        fit = list(fit[0:population_size])

        # print best fitness
        print("0080: best fitness values in generation ", gen, "is", fit[0], fit[1], fit[2], fit[3])

    print(fit)
    time_consumed = time.time() - start_time
    print('time consumed', time_consumed)
    return (pop[0])


def calc_EA_tour(tsp):
    return path_length(tsp, EA_tour(tsp, 20, 5000))
