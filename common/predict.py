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

def formatDataSimple(data):

    data = data[data['PlayType'] != 'Timeout']
    data = data[data['PlayType'] != 'Two Minute Warning']
    data = data[data['PlayType'] != 'Quarter End']
    data = data[data['PlayType'] != 'End of Game']
    data = data[data['PlayType'] != 'No Play']
    data = data[data['PlayType'] != 'Kickoff']
    data = data[data['PlayType'] != 'Extra Point']
    data = data[data['PlayType'] != 'Onside Kick']

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

def formatDataComplex(data):

    data = data[data['PlayType'] != 'Timeout']
    data = data[data['PlayType'] != 'Two Minute Warning']
    data = data[data['PlayType'] != 'Quarter End']
    data = data[data['PlayType'] != 'End of Game']
    data = data[data['PlayType'] != 'No Play']
    data = data[data['PlayType'] != 'Kickoff']
    data = data[data['PlayType'] != 'Extra Point']
    data = data[data['PlayType'] != 'Onside Kick']

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
    data['passed'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Short') & (data['PassLocation'] == 'right')] = 1
    data['passed'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Short') & (data['PassLocation'] == 'middle')] = 2
    data['passed'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Short') & (data['PassLocation'] == 'left')] = 3
    data['passed'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Deep') & (data['PassLocation'] == 'right')] = 4
    data['passed'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Deep') & (data['PassLocation'] == 'middle')] = 5
    data['passed'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Deep') & (data['PassLocation'] == 'left')] = 6

    data['passed'][data['PlayType'] == 'Sack'] = 7


    data['passed'][data['PlayType'] == 'Run'] = 10
    data['passed'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'right') & (data['RunGap'] == 'end')] = 11
    data['passed'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'right') & (data['RunGap'] == 'tackle')] = 12
    data['passed'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'right') & (data['RunGap'] == 'guard')] = 13
    data['passed'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'middle')] = 14
    data['passed'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'left') & (data['RunGap'] == 'guard')] = 15
    data['passed'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'left') & (data['RunGap'] == 'tackle')] = 16
    data['passed'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'left') & (data['RunGap'] == 'end')] = 17

    data['passed'][data['PlayType'] == 'Punt'] = 20
    data['passed'][data['PlayType'] == 'Field Goal'] = 30
    data['passed'][data['PlayType'] == 'QB Kneel'] = 40

    data['success'] = 0
    data['success'][((data['down'] == 1) | (data['down'] == 2)) & (data['Yards.Gained'] >= 4) & (data['InterceptionThrown'] == 0) & (data['Fumble'] = 0)] = 1
    data['success'][(data['Touchdown'] == 1) & (data['InterceptionThrown'] == 0) & (data['Fumble'] = 0)] = 1
    data['success'][(data['FirstDown'] == 1) & (data['down'] < 4) & (data['InterceptionThrown'] == 0) & (data['Fumble'] = 0)] = 1
    data['success'][(data['PlayType'] == 'Field Goal') & (data['FieldGoalResult'] == 'Good')]

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

def makeComplexForest(train):
    target = train['passed'].values
    features = train[['posteamint', 'down', 'ydstogo', 'yrdline100', 'ScoreDiff', 'TimeSecs']].values

    my_forest = RandomForestClassifier(max_depth = 20, min_samples_split=2, n_estimators = 100, random_state = 1)
    my_forest = my_forest.fit(features, target)

    joblib.dump(my_forest, 'data/complex_forest.pkl')

    return my_forest

def makeSimpleForest(train):
    target = train['passed'].values
    features = train[['posteamint', 'down', 'ydstogo', 'yrdline100', 'ScoreDiff', 'TimeSecs']].values

    my_forest = RandomForestClassifier(max_depth = 20, min_samples_split=2, n_estimators = 100, random_state = 1)
    my_forest = my_forest.fit(features, target)

    joblib.dump(my_forest, 'data/simple_forest.pkl')

    return my_forest

def testForest(test, forest=None):
    if forest is None:
        forest = joblib.load('data/simple_forest.pkl')
    target = test['passed'].values
    features = test[['posteamint', 'down', 'ydstogo', 'yrdline100', 'ScoreDiff', 'TimeSecs']].values
    return forest.score(features, target)

def predictSimpleForest(features, forest=None):
    if forest is None:
        forest = joblib.load('common/data/simple_forest.pkl')
    return forest.predict_proba(features)

def predictComplexForest(features, forest=None):
    if forest is None:
        forest = joblib.load('common/data/complex_forest.pkl')
    return forest.predict_proba(features)

def goSimpleForest():
    data = loadData()
    train, test = formatDataSimple(data)
    my_forest = makeSimpleForest(train)
    return testForest(test, my_forest)

def goComplexForest():
    data = loadData()
    train, test = formatDataComplex(data)
    my_forest = makeComplexForest(train)
    return testForest(test, my_forest)

def makeSuccessForest():
    pass
