from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt

from resources.todo import Todo
from resources.predict import Predict

import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from models import User

CORS(app)
api = Api(app)

api.add_resource(Todo, '/<todo_id>')
api.add_resource(Predict, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
