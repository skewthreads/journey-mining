from preprocess import haversine, draw_trip
from tripStructs import Trip
from draw import *
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

def LCS(t1, t2):
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
    return C

def backTrack(C, t1, t2, i, j):
    if i == 0 or j == 0:
        return []
    elif haversine(t1[i-1][1], t1[i-1][2], t2[j-1][1], t2[j-1][2]) < 0.2:
        return backTrack(C, t1, t2, i-1, j-1) + [t1[i-1]]
    else:
        if C[i][j-1] > C[i-1][j]:
            return backTrack(C, t1, t2, i, j-1)
        else:
            return backTrack(C, t1, t2, i-1, j)

def find_neighbors(k):
    with open('datasets/test_set_a1.csv', 'r') as inputFile, open('datasets/tripsClean.csv', 'r') as inputClean:
        next(inputFile)
        testSet = csv.reader(inputFile, delimiter=';')
        tripsClean = csv.reader(inputClean, delimiter=';')
        test_tripID = 0
        for testTrip in testSet:
            test_tripID += 1
            test_timeseries = ast.literal_eval(testTrip[0])
            neighbors = []
            inputClean.seek(0) # Start from the top again
            for cleanTrip in tripsClean:
                clean_tripID = cleanTrip[0]
                clean_journeyPatternID = cleanTrip[1]
                clean_timeseries = ast.literal_eval(cleanTrip[2])
                distance = DTWDistance(test_timeseries, clean_timeseries)
                neighbors.append((distance, clean_journeyPatternID, clean_timeseries))
            neighbors.sort(key=lambda tup: tup[0])
            neighbors = neighbors[:k]
            draw_trip(test_timeseries, test_tripID)
            for n in neighbors:
                draw_trip(n[2], str(test_tripID)+'_'+n[1]+ '_neighbor')

def find_subsequences(k):
    with open('datasets/test_set_a2.csv', 'r') as inputFile, open('datasets/tripsClean.csv', 'r') as inputClean:
        next(inputFile)
        testSet = csv.reader(inputFile, delimiter=';')
        tripsClean = csv.reader(inputClean, delimiter=';')
        test_tripID = 0
        for testTrip in testSet:
            test_tripID += 1
            test_timeseries = ast.literal_eval(testTrip[0])
            subsequences = []
            inputClean.seek(0) # Start from the top again
            for cleanTrip in tripsClean:
                clean_tripID = cleanTrip[0]
                clean_journeyPatternID = cleanTrip[1]
                clean_timeseries = ast.literal_eval(cleanTrip[2])
                C = LCS(test_timeseries, clean_timeseries)
                n = len(test_timeseries)
                m = len(clean_timeseries)
                matchingPoints = C[n][m]
                subsequence = backTrack(C, test_timeseries, clean_timeseries, len(test_timeseries), len(clean_timeseries))
                subsequences.append((matchingPoints, subsequence, clean_timeseries, clean_tripID))
            subsequences.sort(reverse=True)
            subsequences = subsequences[:k]
            draw_trip(test_timeseries, test_tripID)
            for s in subsequences:
                draw_overlapping_trips(s[2], s[1], str(test_tripID)+'_'+s[3]+ '_neighbor')


# find_neighbors(5)
# find_subsequences(5)
