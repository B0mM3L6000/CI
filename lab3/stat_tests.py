import scipy.stats as ss
import numpy as np



# import data

def getdata(path):
    datalist =[]
    data = open(path, "r")
    for line in data:
        line = line.rstrip()
        line = float(line)
        datalist.append(line)
    data.close()
    return datalist

#inputs für data (auskommentiert bei tests vorerst):
"""
path_a = input("Dateiname A? (Beispiel: data_A.txt)")
path_b = input("Dateiname B? (Beispiel: data_B.txt)")
"""
#hardcoded für tests zum zeitsparen
path_a = "data_A.txt"
path_b = "data_B.txt"

data_a = getdata(path_a)
data_b = getdata(path_b)

#data_a = [0.03,0.91,0.64,0.99,0.64,0.16,0.16,0.91,0.16,0.27]
#data_b = [0.64,0.08,0.16,0.27,0.02,0.01,0.16,0.03,0.03,0.64]

#alpha = float(input("Welches Alpha?"))
alpha = 0.05

#print(path_a)
#print(path_b)

#print(alpha)

#######################################################################
#sort data:
data_a_sorted = sorted(data_a)
data_b_sorted = sorted(data_b)

#print data:
print("*****************Data*****************")
print("Datapoints A:", data_a)
print("Datapoints B:", data_b)
print("")

#print sorted data:
print("*****************Sorted Data*****************")
print("Sorted Data A:", data_a_sorted)
print("Sorted Data B:", data_b_sorted)
print("")

#######################################################################

def ranks(a, b):
    ranks_a = []
    ranks_b = []

    sequence_a = sorted(a)
    sequence_b = sorted(b)

    sequence_both = sorted(a+b)
    ranks_both = ss.rankdata(sequence_both)

    for i in range(len(sequence_a)):
        for j in range(len(sequence_both)):
            if sequence_a[i] == sequence_both[j]:
                ranks_a.append(ranks_both[j])
                break
        continue

    for i in range(len(sequence_b)):
        for j in range(len(sequence_both)):
            if sequence_b[i] == sequence_both[j]:
                ranks_b.append(ranks_both[j])
                break
        continue

    return ranks_a, ranks_b

ranksA, ranksB = ranks(data_a,data_b)

print("*****************Ranks*****************")
print("a:", data_a_sorted)
print("ranks a:", ranksA)
print("")
print("b:", data_b_sorted)
print("ranks b:", ranksB)
print("")

#######################################################################
#Tests:

def test_all(a, b, alpha = 0.05):
    mean_a = np.mean(a)
    mean_b = np.mean(b)

    return mean_a, mean_b

#Rankedbased Tests:

def test_all2(a, b, alpha = 0.05):
    rankA, rankB = ranks(a,b)

    return

#print results

def print_results_raw(alpha,mean_a,mean_b):
    print("*****************Full analysis of raw data*****************")
    print("Alpha:", alpha)
    # Sequence A:
    print("")
    print("***Sequence A:")
    print("")
    print("Mean:\t", round(mean_a, 4))

    # Sequence B:
    print("")
    print("***Sequence B:")
    print("")
    print("Mean:\t", round(mean_b, 4))

    return

def print_results_ranks(alpha, mean_a, mean_b):
    print("*****************Full analysis of rank data*****************")
    print("Alpha:", alpha)

    #Sequence A:
    print("")
    print("***Sequence A:")
    print("")
    print("Mean:\t",round(mean_a, 4))

    #Sequence B:
    print("")
    print("***Sequence B:")
    print("")
    print("Mean:\t",round(mean_b, 4))


    return

mean_a, mean_b = test_all(data_a, data_b, alpha)
print_results_raw(alpha, mean_a, mean_b)


"""
mean_a, mean_b = test_all2(data_a, data_b, alpha)
print_results_ranks(alpha, mean_a, mean_b)
"""