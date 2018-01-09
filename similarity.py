from preprocess import haversine, Trip
import csv
import ast

def DTWDistance(t1, t2):
    n = len(t1)
    m = len(t2)
    dtw = [[None for i in range(m+1)] for j in range(n+1)]
    for i in range(1,n+1):
        dtw[i][0] = float('inf')
    for i in range(1,m+1):
        dtw[0][i] = float('inf')
    dtw[0][0] = 0
    for i in range(1,n+1):
        for j in range(1,m+1):
            cost = haversine(t1[i-1][1], t1[i-1][2], t2[j-1][1], t2[j-1][2])
            dtw[i][j] = cost + min(dtw[i-1][j], dtw[i][j-1], dtw[i-1][j-1])
    return dtw[n][m]

def LCSLength(t1, t2):
    n = len(t1)
    m = len(t2)
    # An (n+1) times (m+1) matrix
    C = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n+1):
        for j in range(1, m+1):
            distance = haversine(t1[i-1][1], t1[i-1][2], t2[j-1][1], t2[j-1][2])
            if distance < 0.2:
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C[n][m]

def find_neighbors(k):
    with open('datasets/test_set_a1.csv', 'r') as inputFile, open('datasets/tripsClean.csv', 'r') as inputClean:
        testSet = csv.reader(inputFile, delimiter=';')
        tripsClean = csv.reader(inputClean, delimiter=';')
        for testTrip in testSet:
            test_tripID = testTrip[0]
            test_timeseries = ast.literal_eval(testTrip[1])
            distances = []
            for cleanTrip in tripsClean:
                clean_tripID = cleanTrip[0]
                clean_journeyPatternID = cleanTrip[1]
                clean_timeseries = ast.literal_eval(cleanTrip[2])
                distance = DTWDistance(test_timeseries, clean_timeseries)
                distances.append((distance, clean_journeyPatternID, Trip(clean_tripID, clean_timeseries)))
            distances.sort(key=lambda tup: tup[0])
            distances = distances[:k]
            # print('Neighbors of', test_tripID)
            # print(distances)
            neighbors = [distance[2] for distance in distances]
            return neighbors
