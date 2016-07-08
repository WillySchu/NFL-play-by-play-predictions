from flask_restful import reqparse, Resource

from common.predict import predict

import json

parser = reqparse.RequestParser()
parser.add_argument('posteamint')
parser.add_argument('down')
parser.add_argument('ydstogo')
parser.add_argument('yrdline100')
parser.add_argument('ScoreDiff')
parser.add_argument('TimeSecs')
parser.add_argument('play')

class PredictComplex(Resource):
    def post(self):
        args = parser.parse_args()
        features = [args['posteamint'], args['down'], args['ydstogo'], args['yrdline100'], args['ScoreDiff'], args['TimeSecs']]
        prediction = predict(features, 'play')[0]
        return json.dumps(prediction.tolist())

class PredictSimple(Resource):
    def post(self):
        args = parser.parse_args()
        features = [args['posteamint'], args['down'], args['ydstogo'], args['yrdline100'], args['ScoreDiff'], args['TimeSecs']]
        prediction = predict(features, 'passed')[0]
        return json.dumps(prediction.tolist())

class PredictSuccess(Resource):
    def post(self):
        args = parser.parse_args()
        features = [args['posteamint'], args['down'], args['ydstogo'], args['yrdline100'], args['ScoreDiff'], args['TimeSecs'], args['play']]
        prediction = predict(features, 'passed_success')[0]
        return json.dumps(prediction.tolist())
