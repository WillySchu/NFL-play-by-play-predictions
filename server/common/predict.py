import pandas as pd
from datetime import datetime
import itertools
import numpy as np
from sklearn import tree
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier

def loadData(data='nflplaybyplay2015.csv', low_memory = False):
    return pd.read_csv(data)

def formatData(data):

    teams = {
        'ARI': 0,
        'ATL': 1,
        'BAL': 2,
        'BUF': 3,
        'CAR': 4,
        'CHI': 5,
        'CIN': 6,
        'CLE': 7,
        'DAL': 8,
        'DEN': 9,
        'DET': 10,
        'GB': 11,
        'HOU': 12,
        'IND': 13,
        'JAX': 14,
        'KC': 15,
        'MIA': 16,
        'MIN': 17,
        'NE': 18,
        'NO': 19,
        'NYG': 20,
        'NYJ': 21,
        'OAK': 22,
        'PHI': 23,
        'PIT': 24,
        'SD': 25,
        'SEA': 26,
        'SF': 27,
        'STL': 28,
        'TB': 29,
        'TEN': 30,
        'WAS': 31
    }

    data = data[data['PlayType'] != 'Timeout']
    data = data[data['PlayType'] != 'Two Minute Warning']

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
    data['TimeSecs'][np.isnan(data['TimeSecs']) == True] = 0

    train = data[data['week'] != 11]
    test = data[data['week'] == 11]

    return (train, test)

def makeTree(train):
    target = train['passed'].values
    features = train[['down', 'ydstogo', 'ScoreDiff', 'TimeSecs']].values

    my_tree = tree.DecisionTreeClassifier()
    my_tree = my_tree.fit(features, target)

    joblib.dump(my_tree, 'my_tree.pkl')

    return my_tree

def testTree(test, tree=None):
    if tree is None:
        tree = joblib.load('my_tree.pkl')
    target = test['passed'].values
    features = test[['down', 'ydstogo', 'ScoreDiff', 'TimeSecs']].values
    return tree.score(features, target)

def predictTree(features, tree=None):
    if tree is None:
        tree = joblib.load('common/my_tree.pkl')
    return tree.predict(features)

def goTree():
    data = loadData()
    train, test = formatData(data)
    my_tree = makeTree(train)
    return testTree(test, my_tree)

def makeForest(train):
    target = train['passed'].values
    features = train[['down', 'ydstogo', 'ScoreDiff', 'TimeSecs']].values

    my_forest = RandomForestClassifier(max_depth = 10, min_samples_split=2, n_estimators = 100, random_state = 1)
    my_forest = my_forest.fit(features, target)

    joblib.dump(my_forest, 'my_forest.pkl')

    return my_forest

def testForest(test, forest=None):
    if forest is None:
        forest = joblib.load('my_forest.pkl')
    target = test['passed'].values
    features = test[['down', 'ydstogo', 'ScoreDiff', 'TimeSecs']].values
    return forest.score(features, target)

def predictForest(features, forest=None):
    if forest is None:
        forest = joblib.load('my_forest.pkl')
    return forest.predict(features)

def goForest():
    data = loadData()
    train, test = formatData(data)
    my_forest = makeForest(train)
    return testForest(test, my_forest)
