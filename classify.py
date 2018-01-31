import csv
import ast
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
            cellMap = OrderedSet()
            for point in timeseries:
                dy = haversine(float(point[1]), min_lat, min_lon, min_lat)
                dx = haversine(min_lon, float(point[2]), min_lon, min_lat)
                cellMap.add('C'+str(int(dx // cellSide))+','+str(int(dy // cellSide)))
            if len(row) == 3:
                outputWriter.writerow([tripID, journeyPatternID, ';'.join([str(x) for x in cellMap])])
            else: #elif len(row) == 2
                outputWriter.writerow([tripID, ';'.join([str(x) for x in cellMap])])

def classify(classifier):
    df=pd.read_csv('datasets/tripsClean_grid.csv',sep='!')
    le = preprocessing.LabelEncoder()
    le.fit(df['JourneyPatternID'])
    Y_train=le.transform(df['JourneyPatternID'])
    X_train=df['Trajectory']
    vectorizer = HashingVectorizer(binary=True, tokenizer=lambda x: x.split(';'))
    pipeline = Pipeline([
        ('vect', vectorizer),
        ('classifier', classifier)
    ])
    kf = KFold(n_splits=10)
    mean_accuracy = 0
    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)
    all_tpr = []
    fold = 0
    for train_index, test_index in kf.split(X_train):
    	X_train2, X_test = X_train[train_index], X_train[test_index]
    	Y_train2, Y_test = Y_train[train_index], Y_train[test_index]
    	pipeline.fit(X_train2,Y_train2)
    	predicted=pipeline.predict(X_test)
    	acc = accuracy_score(Y_test,predicted)
    	mean_accuracy += acc
    	fold += 1
    mean_accuracy = mean_accuracy / fold
    print "Mean accuracy: ",mean_accuracy


# min_lon, min_lat = (-6.61505, 53.07045)
min_lon, min_lat = find_min_border('datasets/tripsClean.csv')
print 'min: ', (min_lon, min_lat)
# gridify('datasets/tripsClean.csv',(min_lon, min_lat), float(sys.argv[1]))
gridify('datasets/tripsClean.csv',(min_lon, min_lat), 1)
gridify('datasets/test_set.csv',(min_lon, min_lat), 1)

classify(classifier = KNeighborsClassifier())
# classify(classifier = LogisticRegression())
# classify(classifier = RandomForestClassifier(n_estimators = 10, random_state = 1, n_jobs=-1))

