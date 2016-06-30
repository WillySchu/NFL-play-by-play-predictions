from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin

from resources.todo import Todo
from resources.predict import Predict

import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
CORS(app)
api = Api(app)

api.add_resource(Todo, '/<todo_id>')
api.add_resource(Predict, '/')

print(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
