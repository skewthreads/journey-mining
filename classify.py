import csv
import ast

# Find maximum and minimum borders in dataset
def find_borders(inputFile):
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
            temp = max(timeseries, key=lambda x: x[1])
            if max_lon < temp[1]:
                max_lon = temp[1]
            temp = max(timeseries, key=lambda x: x[2])
            if max_lat < temp[2]:
                max_lat = temp[2]
        return (min_lon, min_lat), (max_lon, max_lat)



(min_lon, min_lat), (max_lon, max_lat) = find_borders('datasets/tripsClean.csv')
print "min: ", (min_lon, min_lat)
print "max: ", (max_lon, max_lat)
