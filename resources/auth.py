from flask_restful import reqparse, Resource
from flask import jsonify
from models import User

parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')

class Register(Resource):
    # def post(self):
    #     args = parser.parse_args
    #     user = User(
    #         email=args['email'],
    #         password=args['password']
    #     )
    #     try:
    #         db.session.add(user)
    #         db.session.commit()
    #         status = 'success'
    #     except:
    #         status = 'this user is already registered'
    #     db.session.close()
    #     return jsonify({'result': status})

    def get(self):
        return 'yo'

# class Login(Resource):
#     pass
