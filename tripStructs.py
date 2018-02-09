
class Trip:
    tripID = ''
    timeseries = []
    journeyPatternID = ''

    def __init__(self, tid, point, journeyPatternID):
        self.tripID = tid
        self.timeseries = [point]
        self.journeyPatternID = journeyPatternID

    def add_to_series(self, point):
        self.timeseries.append(point)

    def print_series(self):
        print('\tTID: ' + str(self.tripID))
        print('\tJPID: ' + str(self.journeyPatternID))
        print('\t' + str(self.timeseries))
        print


class Vehicle:
    vehicleID = ''
    trips = []

    def __init__(self, vid, trip):
        self.vehicleID = vid
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

    def getLastJourneyPatternID(self):
        return self.trips[-1].journeyPatternID
