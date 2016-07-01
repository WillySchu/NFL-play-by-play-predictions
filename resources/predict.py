from flask_restful import reqparse, Resource

from common.predict import predictTree
from common.predict import predictForest

import json

parser = reqparse.RequestParser()
parser.add_argument('posteamint')
parser.add_argument('down')
parser.add_argument('ydstogo')
parser.add_argument('yrdline100')
parser.add_argument('ScoreDiff')
parser.add_argument('TimeSecs')

class Predict(Resource):
    def post(self):
        args = parser.parse_args()
        features = [[args['posteamint'], args['down'], args['ydstogo'], args['yrdline100'], args['ScoreDiff'], args['TimeSecs']]]
        prediction = predictForest(features)[0]
        return json.dumps(prediction.tolist())

    def get(self):
        return 'Hello World'
