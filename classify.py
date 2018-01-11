import csv
import ast
from orderedset import OrderedSet
from preprocess import haversine

# Find minimum borders in dataset
def find_min_border(inputFile):
    with open(inputFile, 'r') as inFile:
        next(inFile)
        inputReader = csv.reader(inFile, delimiter=';')
        min_lon = float('inf')
        min_lat = float('inf')
        for row in inputReader:
            timeseries = ast.literal_eval(row[2])
            temp = min(timeseries, key=lambda x: x[1])
            if min_lon > temp[1]:
                min_lon = temp[1]
            temp = min(timeseries, key=lambda x: x[2])
            if min_lat > temp[2]:
                min_lat = temp[2]
        return min_lon, min_lat

def gridify(filename, (min_lon, min_lat), cellSide): #cellSide in km
    with open(filename, 'r') as inFile, open(filename[:-4]+'_grid.csv', 'w') as outFile:
        first = next(inFile)
        inputReader = csv.reader(inFile, delimiter=';')
        outputWriter = csv.writer(outFile, delimiter='!') # Changed delimiter
        outputWriter.writerow(first[:-1].split(';'))
        for row in inputReader:
            tripID = row[0]
            if len(row) == 3:
                journeyPatternID = row[1]
                timeseries = ast.literal_eval(row[2])
            else: #elif len(row) == 2
                timeseries = ast.literal_eval(row[1])

            cellMap = OrderedSet()
            for point in timeseries:
                dy = haversine(point[1], min_lat, min_lon, min_lat)
                dx = haversine(min_lon, point[2], min_lon, min_lat)
                cellMap.add('C'+str(int(dx // cellSide))+','+str(int(dy // cellSide)))
            if len(row) == 3:
                outputWriter.writerow([tripID, journeyPatternID, ';'.join([str(x) for x in cellMap])])
            else: #elif len(row) == 2
                outputWriter.writerow([tripID, ';'.join([str(x) for x in cellMap])])



min_lon, min_lat = find_min_border('datasets/tripsClean.csv')
print "min: ", (min_lon, min_lat)
gridify('datasets/tripsClean.csv',(min_lon, min_lat), 1.5)
gridify('datasets/test_set.csv',(min_lon, min_lat), 1.5)
