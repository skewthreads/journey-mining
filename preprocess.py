#!/usr/bin/python
import csv
import ast
from draw import *
from tripStructs import *
from math import radians, cos, sin, asin, sqrt

# Calculate the great circle distance between two points on the earth (specified in decimal degrees)
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    a = sin((lat2 - lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1)/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def create_trip_data():
    d = {}
    tripID = 0
    with open('datasets/train_set.csv', 'r') as inputFile:
        next(inputFile)
        dataReader = csv.reader(inputFile)
        for row in dataReader:
            journeyPatternID = row[0]
            vehicleID = row[1]
            timestamp = row[2]
            lon = row[3]
            lat = row[4]
            if journeyPatternID == 'null' or journeyPatternID == '':
                continue
            if vehicleID not in d:
                d[vehicleID] = Vehicle(vehicleID, journeyPatternID, Trip(tripID, [timestamp, lon, lat]))
                tripID += 1
            else:
                vehicle = d[vehicleID]
                if journeyPatternID == vehicle.journeyPatternID:
                    vehicle.append_to_last_trip([timestamp, lon, lat])
                else:
                    vehicle.journeyPatternID = journeyPatternID
                    vehicle.add_trip(Trip(tripID, [timestamp, lon, lat]))
                    tripID += 1
    # parse into list
    dictID = {}
    for vehicleID, vehicle in d.iteritems():
        for trip in vehicle.trips:
            dictID[trip.tripID] = [vehicle.journeyPatternID, trip.timeseries]
    with open('datasets/trips.csv', 'w') as outFile:
        dataWriter = csv.writer(outFile, delimiter=';')
        dataWriter.writerow(['TripID', 'JourneyPatternID', 'Trajectory'])
        for tid in range(len(dictID)):
            trip = dictID[tid]
            timeseries = trip[1]
            dataWriter.writerow([tid, trip[0],timeseries])

def clean_trip_data():
    with open('datasets/trips.csv', 'r') as inputFile, open('datasets/tripsClean.csv', 'w') as outputFile:
        next(inputFile)
        dataReader = csv.reader(inputFile, delimiter=';')
        dataWriter = csv.writer(outputFile, delimiter=';')
        dataWriter.writerow(['TripID','JourneyPatternID','Trajectory']) # write header
        for row in dataReader:
            tripID = row[0]
            journeyPatternID = row[1]
            timeseries = ast.literal_eval(row[2])
            totalDistance = 0
            maxDistance = 0
            for i in range(len(timeseries) - 1):
                distance = haversine(float(timeseries[i][1]), float(timeseries[i][2]), float(timeseries[i+1][1]), float(timeseries[i+1][2]))
                if distance > maxDistance:
                    maxDistance = distance
                totalDistance += distance
            if totalDistance >= 2 and maxDistance <= 2:
                dataWriter.writerow([tripID, journeyPatternID, timeseries])


def main():
    create_trip_data()
    clean_trip_data()
    draw_n_trips(5)


if __name__ == '__main__':
	main()
