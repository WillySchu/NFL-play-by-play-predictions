from flask_restful import reqparse, Resource
from flask import jsonify, session
from models import User
from app import db, bcrypt

parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')

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
        except:
            status = 'this user is already registered'
        db.session.close()
        return jsonify({'result': status})

class Login(Resource):
    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if user and bcrypt.check_password_hash(
                user.password, args['password']):
            session['logged_in'] = True
            status = True
        else:
            status = False
        return jsonify({'result': status})


class Logout(Resource):
    def post(self):
        session.pop('logged_in', None)
        return jsonify({'result': 'success'})
