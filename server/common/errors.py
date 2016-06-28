from flask_restful import abort

from common.todos import todos

def abort_if_no_todo(todo_id):
    if todo_id not in todos:
        abort(404, message='Todo {} does not exist'.format(todo_id))
