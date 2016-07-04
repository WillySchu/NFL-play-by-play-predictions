import pandas as pd
from datetime import datetime
import itertools
import numpy as np
from sklearn import tree
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier

teamLabels = None

def loadData(data='nflplaybyplay2015.csv', low_memory = False):
    return pd.read_csv(data)

def formatData(data):

    data = data[data['PlayType'] != 'Timeout']
    data = data[data['PlayType'] != 'Two Minute Warning']
    data = data[data['PlayType'] != 'Quarter End']
    data = data[data['PlayType'] != 'End of Game']
    data = data[data['PlayType'] != 'No Play']
    data = data[data['PlayType'] != 'Kickoff']

    labels, levels = pd.factorize(data['posteam'])
    teamLabels = levels
    data['posteamint'] = labels

    def week(date):
        startDate = '2015-09-10'
        return (datetime.strptime(date,'%Y-%m-%d')
        - datetime.strptime(startDate, '%Y-%m-%d')).days // 7

    data['week'] = 0
    data['week'] = [week(t) for t in data['Date']]

    data['passed'] = 0
    data['passed'][data['PlayType'] == 'Pass'] = 0
    data['passed'][data['PlayType'] == 'Sack'] = 0
    data['passed'][data['PlayType'] == 'Run'] = 1
    data['passed'][data['PlayType'] == 'Punt'] = 2
    data['passed'][data['PlayType'] == 'Field Goal'] = 3


    data['down'][np.isnan(data['down']) == True] = 0
    data['ScoreDiff'][np.isnan(data['ScoreDiff']) == True] = 0
    data['TimeSecs'][np.isnan(data['TimeSecs']) == True] = 0

    train = data[data['week'] != 11]
    test = data[data['week'] == 11]

    return (train, test)

def makeTree(train):
    target = train['passed'].values
    features = train[['posteamint', 'down', 'ydstogo', 'yrdline100', 'ScoreDiff', 'TimeSecs']].values

    my_tree = tree.DecisionTreeClassifier()
    my_tree = my_tree.fit(features, target)

    joblib.dump(my_tree, 'data/my_tree.pkl')

    return my_tree

def testTree(test, tree=None):
    if tree is None:
        tree = joblib.load('my_tree.pkl')
    target = test['passed'].values
    features = test[['posteamint', 'down', 'ydstogo', 'yrdline100', 'ScoreDiff', 'TimeSecs']].values
    return tree.score(features, target)

def predictTree(features, tree=None):
    if tree is None:
        tree = joblib.load('common/data/my_tree.pkl')
    return tree.predict_proba(features)

def goTree():
    data = loadData()
    train, test = formatData(data)
    my_tree = makeTree(train)
    return testTree(test, my_tree)

def makeForest(train):
    target = train['passed'].values
    features = train[['posteamint', 'down', 'ydstogo', 'yrdline100', 'ScoreDiff', 'TimeSecs']].values

    my_forest = RandomForestClassifier(max_depth = 20, min_samples_split=2, n_estimators = 100, random_state = 1)
    my_forest = my_forest.fit(features, target)

    joblib.dump(my_forest, 'data/my_forest.pkl')

    return my_forest

def testForest(test, forest=None):
    if forest is None:
        forest = joblib.load('data/my_forest.pkl')
    target = test['passed'].values
    features = test[['posteamint', 'down', 'ydstogo', 'yrdline100', 'ScoreDiff', 'TimeSecs']].values
    return forest.score(features, target)

def predictForest(features, forest=None):
    if forest is None:
        forest = joblib.load('common/data/my_forest.pkl')
    return forest.predict_proba(features)

def goForest():
    data = loadData()
    train, test = formatData(data)
    my_forest = makeForest(train)
    return testForest(test, my_forest)
