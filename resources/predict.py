from flask_restful import reqparse, Resource

from common.predict import predictTree
from common.predict import predictForest

parser = reqparse.RequestParser()
parser.add_argument('down')
parser.add_argument('ydstogo')
parser.add_argument('ScoreDiff')
parser.add_argument('TimeSecs')

class Predict(Resource):
    def post(self):
        args = parser.parse_args()
        features = [[args['down'], args['ydstogo'], args['ScoreDiff'], args['TimeSecs']]]
        return predictForest(features)[0]

    def get(self):
        return 'Hello World'
