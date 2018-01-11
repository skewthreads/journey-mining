import csv
import ast

# Find minimum borders in dataset
def find_min_boarder(inputFile):
    with open(inputFile, 'r') as inFile:
        inputReader = csv.reader(inFile, delimiter=';')
        min_lon = float('inf')
        min_lat = float('inf')
        max_lon = float('-inf')
        max_lat = float('-inf')
        for row in inputReader:
            timeseries = ast.literal_eval(row[2])
            temp = min(timeseries, key=lambda x: x[1])
            if min_lon > temp[1]:
                min_lon = temp[1]
            temp = min(timeseries, key=lambda x: x[2])
            if min_lat > temp[2]:
                min_lat = temp[2]
        return min_lon, min_lat


min_lon, min_lat = find_min_boarder('datasets/tripsClean.csv')
print "min: ", (min_lon, min_lat)
