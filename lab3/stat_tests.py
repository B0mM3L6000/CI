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

#print sorted data:
print("*****************Sorted Data*****************")
print("Sorted Data A:", data_a_sorted)
print("Sorted Data B:", data_b_sorted)


#######################################################################
#Tests:

def test_all(a, b, alpha = 0.05):
    return

#Rankedbased Tests:

def test_all2(a, b, alpha = 0.05):
    return

#print results

test_all(data_a, data_b, alpha)
test_all2(data_a, data_b, alpha)