#!/usr/bin/python3
import csv

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

def main():
    d = {}
    tripID = 0
    with open('datasets/train_set.csv', 'r') as csvfile:
        dataReader = csv.reader(csvfile, delimiter=',')
        for row in dataReader:
            journeyPatternID = row[0]
            vehicleID = row[1]
            timestamp = row[2]
            lon = row[3]
            lat = row[4]
            if journeyPatternID == 'null':
                continue
            if vehicleID not in d:
                d[vehicleID] = Vehicle(vehicleID, journeyPatternID, Trip(tripID, [timestamp, lon, lat]))
            else:
                vehicle = d[vehicleID]
                if journeyPatternID == vehicle.journeyPatternID:
                    vehicle.append_to_last_trip([timestamp, lon, lat])
                else:
                    vehicle.journeyPatternID = journeyPatternID
                    tripID += 1
                    vehicle.add_trip(Trip(tripID, [timestamp, lon, lat]))


if __name__ == '__main__':
	main()
