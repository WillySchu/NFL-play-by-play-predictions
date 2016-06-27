import pandas as pd
from datetime import datetime
import itertools

data = pd.read_csv('')
startDate = '2015-09-10'

def week(date):
    return (datetime.strptime(date,'%Y-%m-%d')
            - datetime.strptime(startDate, '%Y-%m-%d')).days // 7
