from flask import (Blueprint, request, jsonify, abort)
from core.db import get_db

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

error = {'status': 'error'}
success = {'status': 'success'}


def db_tasks_to_json(tasks):
    res = []
    for task in tasks:
        res.append({'id': task['id'], 'title': task['title'], 'description': task['description']})
    return res


@bp.route('', methods=['GET', 'POST'])
def all_tasks():
    db = get_db()
    if request.method == 'GET':
        tasks = db.execute('SELECT id, title, description FROM task').fetchall()
        success['tasks'] = db_tasks_to_json(tasks)
        return jsonify(success)
    if request.method == 'POST':
        task = request.get_json()
        if 'title' not in task:
            abort(400, description='No title provided.')
        if 'description' not in task:
            abort(400, description='No description provided.')
        try:
            db.execute('INSERT INTO task (title, description) VALUES (?, ?)', (task['title'], task['description']))
            db.commit()
        except db.IntegrityError:
            abort(400, message=f'Title {task["title"]} is already registered.')
        else:
            return jsonify(success)


@bp.route('/<task_id>', methods=['PUT', 'DELETE'])
def modify_task(task_id):
    db = get_db()

    exists = db.execute('SELECT * FROM task WHERE id = ?', [task_id]).fetchone()
    if not exists:
        abort(400, description=f'Id {task_id} is not a valid id.')

    if request.method == 'PUT':
        task = request.get_json()
        query_parts = []
        params = []

        if 'title' in task:
            query_parts.append('title = ?')
            params.append(task['title'])
        if 'description' in task:
            query_parts.append('description = ?')
            params.append(task['description'])
        if not query_parts:
            abort(400, description='No data provided. Provide at least one of title or description.')

        query = f'UPDATE task SET {", ".join(query_parts)} WHERE ID = ?'
        params.append(task_id)

        try:
            db.execute(query, params)
            db.commit()
        except db.IntegrityError:
            abort(400, description=f'Title {task["title"]} is already registered')

        return jsonify(success)

    if request.method == 'DELETE':
        db.execute('DELETE FROM task WHERE id = ?', [task_id])
        db.commit()
        return jsonify(success)
