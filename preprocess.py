

class Trip:
    tripID = ''
    timeseries = []

    def __init__(self, tid, point):
        self.tripID = tid
        self.timeseries = [point]

    def add_to_series(self, point):
        self.timeseries.append(point)

    def print_series(self):
        print('TID: ' + str(self.tripID))
        print(self.timeseries)
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
        self.timeseries.append(trip)

