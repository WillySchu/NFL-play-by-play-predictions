from flask_restful import reqparse, Resource
from flask import jsonify, session

from models import User
from app import db, bcrypt

parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')
parser.add_argument('token')

class Register(Resource):
    def post(self):
        args = parser.parse_args()
        print(args)
        user = User(
            email=args['email'],
            password=args['password']
        )
        try:
            db.session.add(user)
            db.session.commit()
            status = 'success'
            token = user.generate_auth_token()
            db.session.close()
            return jsonify({'id': user.id, 'email': user.email, 'token': token})
        except:
            status = False
        return jsonify(status)

class Login(Resource):
    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if user and bcrypt.check_password_hash(
                user.password, args['password']):
            session['logged_in'] = True
            userDict = user.__dict__
            token = user.generate_auth_token()
            return jsonify({'id': userDict['id'], 'email': userDict['email'], 'favteam': userDict['favteam'], 'token': token});
        else:
            status = False
        return jsonify(status)


class Logout(Resource):
    def get(self):
        session.pop('logged_in', None)
        return jsonify('success')

class Status(Resource):
    def post(self):
        args = parser.parse_args()
        user = User.verify_auth_token(args['token'])
        return jsonify({'id': user.id, 'email': user.email, 'favteam': user.favteam})
