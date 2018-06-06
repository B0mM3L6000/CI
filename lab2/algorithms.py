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


# implements n touirnament selection
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
            parents1.append(list(pop[tournament_selection(fit, 3)])) #auswählen eines elternpaars aus der population mit dem index aus tourney select
            parents2.append(list(pop[tournament_selection(fit, 3)]))

        # pop2=recombine
        print("0040: recombining parents")
        children = [] #kinder initialisieren
        for i in range(0, population_size):
            children.append(recombine(parents1[i], parents2[i])) #elternpaare kombinieren um kinder zu erstellen

        # pop3=mutate
        print("0050: mutating children")
        for i in range(0, population_size):
            node_xchg_step(children[i]) #kinder mutieren

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
