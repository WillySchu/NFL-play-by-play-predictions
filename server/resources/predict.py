from flask_restful import reqparse, Resource

from common.predict import predict

parser = reqparse.RequestParser()
parser.add_argument('down')
parser.add_argument('yrdstogo')
parser.add_argument('ScoreDiff')

class Predict(Resource):
    def post(self):
        args = parser.parse_args()
        print(args)
        print(args['down'])
        print(args['yrdstogo'])
        print(args['ScoreDiff'])
        features = [[args['down'], args['yrdstogo'], args['ScoreDiff']]]
        return predict(features)[0]
