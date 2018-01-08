#!/usr/bin/python
import csv
import gmplot

class Trip:
    tripID = ''
    timeseries = []

    def __init__(self, tid, point):
        self.tripID = tid
        self.timeseries = [point]

    def add_to_series(self, point):
        self.timeseries.append(point)

    def print_series(self):
        print('\tTID: ' + str(self.tripID))
        print('\t' + str(self.timeseries))
        print


class Vehicle:
    vehicleID = ''
    journeyPatternID = ''
    trips = []

    def __init__(self, vid, jpid, trip):
        self.vehicleID = vid
        self.journeyPatternID = jpid
        self.trips = [trip]

    def add_trip(self, trip):
        self.trips.append(trip)

    def append_to_last_trip(self, point):
        self.trips[-1].add_to_series(point)

    def print_trips(self):
        print('VID: ' + str(self.vehicleID))
        for t in self.trips:
            t.print_series()
        print

    def get_last_trip(self):
        return self.trips[-1]

def create_trip_data():
    d = {}
    dictID = {}
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
    for vehicleID, vehicle in d.iteritems():
        for trip in vehicle.trips:
            dictID[trip.tripID] = [vehicle.journeyPatternID, trip.timeseries]
    with open('datasets/trips.csv', 'w') as outFile:
        # dataWriter = csv.writer(outputFile)
        for tid in range(len(dictID)):
            print(tid)
            print(dictID[tid])
            trip = dictID[tid]
            outFile.write(str(tid) + ', ')
            outFile.write(str(trip[0]) + ', [')
            timeseries = trip[1]
            for i in range(len(timeseries) - 1):
                point = timeseries[i]
                outFile.write('[' + str(point[0]) + ', ' + str(point[1]) + ', ' + str(point[2]) + '], ')
            point = timeseries[-1]
            outFile.write('[' + str(point[0]) + ', ' + str(point[1]) + ', ' + str(point[2]) + ']')
            outFile.write(']\n')

def clean_trip_data():
    with open('datasets/trips.csv', 'r') as inputFile, open('datasets/tripsClean.csv', 'w') as outputFile:
        dataReader = csv.reader(inputFile)
        dataWriter = csv.writer(outputFile)
        for row in dataReader:
            tripID = row[0]
            journeyPatternID = row[1]
            timeseries = row[2]

def draw_map(longs, lats):
    gmap = gmplot.GoogleMapPlotter(lats[0], longs[0], 18)
    gmap.plot(lats, longs, 'cornflowerblue', edge_width=10)
    gmap.draw('map.html')

def main():
    create_trip_data()
    # clean_trip_data()
    # draw_map(dsad)


if __name__ == '__main__':
	main()
