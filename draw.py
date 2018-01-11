import gmplot
import csv
import ast

def draw_trip(timeseries, name):
    longs = []
    lats = []
    for point in timeseries:
        longs.append(point[1])
        lats.append(point[2])
    gmap = gmplot.GoogleMapPlotter(lats[0], longs[0], 12)
    gmap.plot(lats, longs, 'cornflowerblue', edge_width=6)
    gmap.draw('maps/map_' + str(name) + '.html')


def draw_overlapping_trips(timeseries1, timeseries2, name):
    longs1 = []
    lats1 = []
    for point in timeseries1:
        longs1.append(point[1])
        lats1.append(point[2])
    longs2 = []
    lats2 = []
    for point in timeseries2:
        longs2.append(point[1])
        lats2.append(point[2])
    gmap = gmplot.GoogleMapPlotter(lats1[0], longs1[0], 12)
    gmap.plot(lats1, longs1, 'green', edge_width=6)
    gmap.plot(lats2, longs2, 'red', edge_width=3)
    gmap.draw('maps/overlap_' + str(name) + '.html')


def draw_n_trips(N):
    with open('datasets/tripsClean.csv', 'r') as inputFile:
        next(inputFile) # skip header
        dataReader = csv.reader(inputFile, delimiter=';')
        i = 0
        journeyPatternIDdict = {}
        for row in dataReader:
            journeyPatternID = row[1]
            # if trip exists, choose another one
            if journeyPatternID in journeyPatternIDdict:
                continue
            if i >= N: # if already drawn N trips, break
                break
            journeyPatternIDdict[journeyPatternID] = 1
            timeseries = ast.literal_eval(row[2])
            draw_trip(timeseries, journeyPatternID)
            i += 1
