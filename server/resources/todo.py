from flask_restful import reqparse, Resource

from common.errors import abort_if_no_todo
from common.todos import todos

parser = reqparse.RequestParser()
parser.add_argument('task')

class Todo(Resource):
    def get(self, todo_id):
        abort_if_no_todo(todo_id)
        return todos[todo_id]

    def delete(self, todo_id):
        abort_if_no_todo(todo_id)
        del todos[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        todos[todo_id] = task
        return task, 201
