import random

par1 = [1,2,3,4,5,6,7,8,9,10,11,12]
par2 = [12,11,10,9,8,7,6,5,4,3,2,1]
par3 = [5,9,10,11,1,4,3,2,6,12,7,8]
print(par1)
print(par3)
"""
bound2 = 2
bound1 = 10

newtour = [1,2,3,4,5,6,7,8,9,10,11,12]
print(newtour)

tmptour = newtour[bound2:bound1]

print(tmptour)
tmptour = random.sample(tmptour, len(tmptour))
print(tmptour)
for _ in range(bound2,bound1):
    newtour.pop(bound2)

print(newtour)
for i in range(bound2, bound1):
    newtour.insert(i, tmptour[i-bound2])

print(newtour)
"""
"""
def arbper(tour, p = 0.4):
    #mache eine arbitrary permutation mit wahrscheinlichkeit p
    randomnumber = random.uniform(0,1)
    print(randomnumber)
    newtour = tour
    if randomnumber <= p: #auswählen der grenzen für die arb permutation
        #print("test")
        bound1 = random.randint(0,len(tour)-1)
        bound2 = random.randint(0,len(tour)-1)
        while bound2 == bound1:
            bound2 = random.randint(0,len(tour)-1)
        #print(bound1, bound2)
        if bound2 < bound1: #sortieren
            bound2, bound1 = bound1, bound2
        bound2 += 1 #wichtig für indexe
        #print(bound1, bound2)
        tmptour = newtour[bound1:bound2]#
        #print(tmptour)
        tmptour = random.sample(tmptour, len(tmptour))
        for _ in range(bound1,bound2):
            newtour.pop(bound1)
        for i in range(bound1, bound2):
            newtour.insert(i, tmptour[i-bound1])
    return newtour

tour = arbper(newtour)
print(tour)
"""
"""
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
        #print(tmp)
        if tmp in genes1:
            #print(i)
            genes2.append(parent2[i])
    j = 0
    for i in range(len(newtour)):   #crossoverschritt
        if gaps[i] == 1:
            newtour[i] = genes2[j]
            j += 1
    return newtour



test = uobcrossover(par1, par2)

print(test)
"""

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
    #doppelte einträge markieren (noch zu implentieren) und auf eine zahl reduzieren:
    for i in range(len(table)):
        table[i] = list(set(table[i]))
    print(table)

    #erstellen des kindes:
    #auswahl des ersten allels von parent1:
    tmp = parent1[0]
    print(tmp)
    for i in range(len(parent1)-1):
        print("schleifendurchlauf", i)
        newtour.append(tmp)
        #löschen dieses allels aus dem edge table:
        for _ in range(len(table)):
            if tmp in table[_]:
                table[_].remove(tmp)
        #auswahl neues allel anhand der regel welche nachbarn liste im table am kürzesten ist (und davon die erste)
        indexalt = tmp - 1
        indexkandidaten = table[indexalt]
        print("indexkandidaten:", indexkandidaten)
        indextmp = indexkandidaten[0]
        for x in range(1,len(indexkandidaten)):
            if len(table[indextmp - 1]) > len(table[indexkandidaten[x] - 1]):
                indextmp = indexkandidaten[x]
        tmp = indextmp
        print("auswahl:", tmp)
        #mn,idx = min( (len(table[j]),j) for j in range(len(table)) )
        #print(idx)
        #tmp = #neues allel
    newtour.append(tmp)
    print(table)

    return newtour



test = edge_recomb(par1, par3)
print(test)
