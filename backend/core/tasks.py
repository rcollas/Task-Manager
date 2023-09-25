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
    if len(exists) == 0:
        error['message'] = f'Id {task_id} is not a valid id.'
        return error

    if request.method == 'PUT':
        task = request.get_json()
        if 'title' in task and 'description' in task:
            try:
                db.execute('UPDATE task SET title = ?, description = ? WHERE id = ?',
                           (task['title'], task['description'], task_id))
                db.commit()
            except db.IntegrityError:
                error['message'] = f'Title {task["title"]} is already registered'
                return jsonify(error)
            else:
                return jsonify(success)
        elif 'title' in task:
            try:
                db.execute('UPDATE task SET title = ? WHERE id = ?', (task['title'], task_id))
                db.commit()
            except db.IntegrityError:
                error['message'] = f'Title {task["title"]} is already registered'
                return jsonify(error)
            else:
                return jsonify(success)
        elif 'description' in task:
            db.execute('UPDATE task SET description = ? WHERE id = ?', (task['description'], task_id))
            return jsonify(success)
        else:
            error['message'] = "No data provided. Provide at least on of title or description."
            return jsonify(error)

    if request.method == 'DELETE':
        db.execute('DELETE FROM task WHERE id = ?', [task_id])
        db.commit()
        return jsonify(success)
