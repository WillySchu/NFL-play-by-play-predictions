from flask_restful import reqparse, Resource

from common.errors import abort_if_no_todo
from common.todos import todos

parser = reqparse.RequestParser()
parser.add_argument('task')

class TodoList(Resource):
    def get(self):
        return todos

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(todos.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        todos[todo_id] = {'task': args['task']}
        return todos[todo_id], 201
