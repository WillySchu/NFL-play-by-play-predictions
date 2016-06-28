import pandas as pd
from datetime import datetime
import itertools
import numpy as np
from sklearn import tree

def loadData(data='nflplaybyplay2015.csv', low_memory = False):
    return pd.read_csv(data)

def formatData(data):

    def week(date):
        startDate = '2015-09-10'
        return (datetime.strptime(date,'%Y-%m-%d')
        - datetime.strptime(startDate, '%Y-%m-%d')).days // 7

    data['week'] = 0
    data['week'] = [week(t) for t in data['Date']]

    data['passed'] = 0
    data['passed'][data['PlayType'] == 'Pass'] = 1
    data['passed'][data['PlayType'] == 'Sack'] = 1
    data['passed'][data['PlayType'] == 'Run'] = 2

    data['down'][np.isnan(data['down']) == True] = 0
    data['ScoreDiff'][np.isnan(data['ScoreDiff']) == True] = 0

    train = data[data['week'] != 8]
    test = data[data['week'] == 8]

    return (train, test)

def makeTree(train):
    target = train['passed'].values
    features = train[['down', 'ydstogo', 'ScoreDiff']].values

    my_tree = tree.DecisionTreeClassifier()
    my_tree = my_tree.fit(features, target)

    return my_tree

def testTree(test, tree):
    target = test['passed'].values
    features = test[['down', 'ydstogo', 'ScoreDiff']].values
    return tree.score(features, target)
