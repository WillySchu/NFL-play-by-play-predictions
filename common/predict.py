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

    data['play'] = 0
    data['play'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Short') & (data['PassLocation'] == 'right')] = 1
    data['play'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Short') & (data['PassLocation'] == 'middle')] = 2
    data['play'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Short') & (data['PassLocation'] == 'left')] = 3
    data['play'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Deep') & (data['PassLocation'] == 'right')] = 4
    data['play'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Deep') & (data['PassLocation'] == 'middle')] = 5
    data['play'][(data['PlayType'] == 'Pass') & (data['PassLength'] == 'Deep') & (data['PassLocation'] == 'left')] = 6

    data['play'][data['PlayType'] == 'Sack'] = 7

    data['play'][data['PlayType'] == 'Run'] = 10
    data['play'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'right') & (data['RunGap'] == 'end')] = 11
    data['play'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'right') & (data['RunGap'] == 'tackle')] = 12
    data['play'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'right') & (data['RunGap'] == 'guard')] = 13
    data['play'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'middle')] = 14
    data['play'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'left') & (data['RunGap'] == 'guard')] = 15
    data['play'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'left') & (data['RunGap'] == 'tackle')] = 16
    data['play'][(data['PlayType'] == 'Run') & (data['RunLocation'] == 'left') & (data['RunGap'] == 'end')] = 17

    data['play'][data['PlayType'] == 'Punt'] = 20
    data['play'][data['PlayType'] == 'Field Goal'] = 30
    data['play'][data['PlayType'] == 'QB Kneel'] = 40

    data['success'] = 0
    data['success'][((data['down'] == 1) | (data['down'] == 2)) & (data['Yards.Gained'] >= 4) & (data['InterceptionThrown'] == 0) & (data['Fumble'] == 0)] = 1
    data['success'][(data['Touchdown'] == 1) & (data['InterceptionThrown'] == 0) & (data['Fumble'] == 0) & (data['PlayType'] != 'Punt')] = 1
    data['success'][(data['FirstDown'] == 1) & (data['down'] < 4) & (data['InterceptionThrown'] == 0) & (data['Fumble'] == 0)] = 1
    data['success'][(data['PlayType'] == 'Field Goal') & (data['FieldGoalResult'] == 'Good')] = 1
    data['success'][(data['down'] == 4) & (data['Yards.Gained'] > data['ydstogo']) & (data['InterceptionThrown'] == 0) & (data['Fumble'] == 0) & ((data['PlayType'] == 'Run') | (data['PlayType'] == 'Pass'))] = 1

    data['down'][np.isnan(data['down']) == True] = 0
    data['ScoreDiff'][np.isnan(data['ScoreDiff']) == True] = 0
    data['TimeSecs'][np.isnan(data['TimeSecs']) == True] = 0

    train = data[data['week'] != 11]
    test = data[data['week'] == 11]

    return (train, test)

def makeForest(tar, train):
    target = train[tar].values
    features = train[['posteamint', 'down', 'ydstogo', 'yrdline100', 'ScoreDiff', 'TimeSecs']].values

    my_forest = RandomForestClassifier(max_depth = 20, min_samples_split=2, n_estimators = 100, random_state = 1)
    my_forest = my_forest.fit(features, target)

    path = 'data/{0}_forest.pkl'.format(tar)
    joblib.dump(my_forest, path)

    return my_forest

def testForest(test, target, forest=None):
    if forest is None:
        forest = joblib.load('data/simple_forest.pkl')
    target = test[target].values
    features = test[['posteamint', 'down', 'ydstogo', 'yrdline100', 'ScoreDiff', 'TimeSecs']].values
    return forest.score(features, target)

def goSimple():
    data = loadData()
    train, test = formatData(data)
    my_forest = makeForest('passed', train)
    return testForest(test,'passed', my_forest)

def goComplex():
    data = loadData()
    train, test = formatData(data)
    my_forest = makeForest('play', train)
    return testForest(test, 'play', my_forest)

def makeSuccessForest(feature, train):
    target = train['success'].values
    features = train[['posteamint', 'down', 'ydstogo', 'yrdline100', 'ScoreDiff', 'TimeSecs', feature]].values

    my_forest = RandomForestClassifier(max_depth = 20, min_samples_split=2, n_estimators = 100, random_state = 1)
    my_forest = my_forest.fit(features, target)

    path = 'data/{0}_success_forest.pkl'.format(feature)
    joblib.dump(my_forest, path)

def testSuccessForest(feature, test, forest=None):
    if forest is None:
        forest = joblib.load('data/' + feature + '_success_forest.pkl')
    target = test['success'].values
    features = test[['posteamint', 'down', 'ydstogo', 'yrdline100', 'ScoreDiff', 'TimeSecs', feature]].values
    return forest.score(features, target)

def goSuccess(feature):
    train, test = formatData(loadData())
    my_forest = makeSuccessForest(feature, train)
    return testSuccessForest(feature, test, my_forest)

def predict(features, forest_type=None, forest=None):
    if not (forest_type or forest):
        raise Exception('forest_type or forest required')
    if forest is None:
        path = 'common/data/{0}_forest.pkl'.format(forest_type)
        forest = joblib.load(path)
    return forest.predict_proba([features])
