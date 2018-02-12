import csv
import ast
import time
import pandas as pd
from sklearn import preprocessing
from orderedset import OrderedSet
from preprocess import haversine
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import sys


# Find minimum borders in dataset
def find_min_border(inputFile):
    with open(inputFile, 'r') as inFile:
        next(inFile)
        inputReader = csv.reader(inFile, delimiter=';')
        min_lon = float('inf')
        min_lat = float('inf')
        for row in inputReader:
            timeseries = ast.literal_eval(row[2])
            temp = min(timeseries, key=lambda x: float(x[1]))
            if min_lon > float(temp[1]):
                min_lon = float(temp[1])
            temp = min(timeseries, key=lambda x: float(x[2]))
            if min_lat > float(temp[2]):
                min_lat = float(temp[2])
        return min_lon, min_lat

def gridify(filename, (min_lon, min_lat), cellSide): #cellSide in km
    with open(filename, 'r') as inFile, open(filename[:-4]+'_grid.csv', 'w') as outFile:
        first = next(inFile)
        inputReader = csv.reader(inFile, delimiter=';')
        outputWriter = csv.writer(outFile, delimiter='!') # Changed delimiter
        outputWriter.writerow(first.rstrip().split(';'))
        for row in inputReader:
            tripID = row[0]
            if len(row) == 3:
                journeyPatternID = row[1]
                timeseries = ast.literal_eval(row[2])
            else: #elif len(row) == 2
                timeseries = ast.literal_eval(row[1])
            cellsList = []
            for point in timeseries:
                dy = haversine(float(point[1]), min_lat, min_lon, min_lat)
                dx = haversine(min_lon, float(point[2]), min_lon, min_lat)
                cell = 'C'+str(int(dx // cellSide))+','+str(int(dy // cellSide))
                if len(cellsList) == 0 or cellsList[-1] != cell:
                    cellsList.append(cell)
            if len(row) == 3:
                outputWriter.writerow([tripID, journeyPatternID, ';'.join([x for x in cellsList])])
            else: #elif len(row) == 2
                outputWriter.writerow([tripID, ';'.join([x for x in cellsList])])

def cross_validate(classifier):
    df=pd.read_csv('datasets/tripsClean_grid_v2.csv',sep='!')
    le = preprocessing.LabelEncoder()
    le.fit(df['JourneyPatternID'])
    Y_train=le.transform(df['JourneyPatternID'])
    X_train=df['Trajectory']
    vectorizer = HashingVectorizer(ngram_range=(1,2), tokenizer=lambda x: x.split(';'))
    pipeline = Pipeline([
        ('vect', vectorizer),
        ('classifier', classifier)
    ])
    scores = cross_val_score(pipeline, X_train, Y_train, cv=10)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

def classify(classifier):
    df=pd.read_csv('datasets/tripsClean_grid.csv',sep='!')
    le = preprocessing.LabelEncoder()
    le.fit(df['JourneyPatternID'])
    Y_train=le.transform(df['JourneyPatternID'])
    X_train=df['Trajectory']
    vectorizer = HashingVectorizer(ngram_range=(1,2), tokenizer=lambda x: x.split(';'))
    pipeline = Pipeline([
        ('vect', vectorizer),
        ('classifier', classifier)
    ])
    pipeline.fit(X_train, Y_train)
    df=pd.read_csv('datasets/test_set_grid.csv',sep='!')
    X_test = df['Trajectory']
    predicted_labels = le.inverse_transform(pipeline.predict(X_test))
    with open('datasets/testSet_JourneyPatternIDs.csv', 'w') as outFile:
        outputWriter = csv.writer(outFile, delimiter='\t')
        outputWriter.writerow(['Test_Trip_ID', 'Predicted_JourneyPatternID'])
        trip_id = 0
        for label in predicted_labels:
            outputWriter.writerow([trip_id, label])
            trip_id += 1



def regridify(filename):
    with open(filename, 'r') as inFile, open(filename[:-4]+'_v2.csv', 'w') as outFile:
        first = next(inFile)
        inputReader = csv.reader(inFile, delimiter='!')
        outputWriter = csv.writer(outFile, delimiter='!')
        outputWriter.writerow(first.rstrip().split('!'))
        for row in inputReader:
            tripID = row[0]
            journeyPatternID = row[1]
            trajectory = row[2]
            cells = trajectory.split(';')
            row = [tripID, journeyPatternID]
            newCells = ''
            for i in range(len(cells)-1):
                c1 = cells[i]
                c2 = cells[i+1]
                x1 = c1.split(',')[0][1:]
                y1 = c1.split(',')[1]
                x2 = c2.split(',')[0][1:]
                y2 = c2.split(',')[1]
                newCell = c1;
                if y2 > y1:
                    newCell += 'N'
                elif y2 < y1:
                    newCell += 'S'
                if x2 > x1:
                    newCell += 'E'
                elif x2 < x1:
                    newCell += 'W'
                newCells += newCell+';'
            newCells+=cells[-1]
            outputWriter.writerow(row+[newCells])



# min_lon, min_lat = (-6.61505, 53.07045)
min_lon, min_lat = find_min_border('datasets/tripsClean.csv')
gridify('datasets/tripsClean.csv',(min_lon, min_lat), 0.2)
gridify('datasets/test_set.csv',(min_lon, min_lat), 0.2)
# regridify('datasets/tripsClean_grid.csv')
# regridify('datasets/test_set_grid.csv')

classify(classifier = KNeighborsClassifier(n_neighbors=1))
# classify(classifier = LogisticRegression())
# classify(classifier = RandomForestClassifier(n_estimators = 10, random_state = 1, n_jobs=-1))
