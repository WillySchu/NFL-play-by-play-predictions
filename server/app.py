from flask import Flask
from flask_restful import Api

from resources.todo import Todo
from resources.todoList import TodoList

app = Flask(__name__)
api = Api(app)

api.add_resource(Todo, '/<todo_id>')
api.add_resource(TodoList, '/')

if __name__ == '__main__':
    app.run(debug=True)
