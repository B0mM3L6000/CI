import random

newtour = [1,2,3,4,5,6,7,8,9,10,11,12]
print(newtour)
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
