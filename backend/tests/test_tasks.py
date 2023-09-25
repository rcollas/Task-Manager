import pytest
from core.db import (get_db)
from utils import (get_last_task_row, get_first_task_row)


def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    tasks = response.json['tasks']
    assert isinstance(tasks, list)
    assert all(isinstance(task, dict) for task in tasks)
    assert all('id' and 'description' and 'title' in task for task in tasks)


def test_post_task_missing_content(client):
    response = client.post('/tasks', json={})
    assert response.status_code == 400


def test_post_task_missing_title(client):
    response = client.post('/tasks', json={'description': 'test'})
    assert response.status_code == 400
    assert response.json['message'] == 'No title provided.'


def test_post_title_already_exists(client, app):
    with app.app_context():
        last_row = get_last_task_row()
        response = client.post('/tasks', json={'title': last_row['title'], 'description': 'random'})
        assert response.status_code == 400
        assert response.json['message'] == f'Title {last_row["title"]} is already registered.'


def test_post_task_missing_description(client):
    response = client.post('/tasks', json={'title': 'test'})
    assert response.status_code == 400
    assert response.json['message'] == 'No description provided.'


def test_post_task(client, app):
    title = 'hello'
    description = 'world'
    response = client.post('/tasks', json={'title': title, 'description': description})
    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        task = get_last_task_row()
        assert task['title'] == title
        assert task['description'] == description


def test_put_task(client, app):
    title = 'update'
    description = 'task'
    with app.app_context():
        db = get_db()
        last_id = get_last_task_row()['id']
        response = client.put(f'/tasks/{last_id}', json={'title': title, 'description': description})
        assert response.status_code == 200
        updated_task = db.execute("SELECT * FROM task WHERE id = ?", [last_id]).fetchone()
        assert updated_task['title'] == title
        assert updated_task['description'] == description


def test_put_task_missing_content(client, app):
    with app.app_context():
        last_id = get_last_task_row()['id']
        response = client.put(f'/tasks/{last_id}', json={})
        assert response.status_code == 400
        assert response.json['message'] == 'No data provided. Provide at least one of title or description.'


def test_put_task_wrong_id(client, app):
    with app.app_context():
        last_id = get_last_task_row()['id']
        response = client.put(f'/tasks/{last_id + 1}', json={'title': 'new', 'description': 'world'})
        assert response.status_code == 400
        assert response.json['message'] == f'Id {last_id + 1} is not a valid id.'


def test_put_task_title_already_exists(client, app):
    with app.app_context():
        last_task = get_last_task_row()
        first_task = get_first_task_row()
        response = client.put(f'/tasks/{last_task["id"]}',
                              json={'title': first_task['title'], 'description': 'a description'})
        assert response.status_code == 400
        assert response.json['message'] == f'Title {first_task["title"]} is already registered'


def test_delete_task(client, app):
    with app.app_context():
        last_id = get_last_task_row()['id']
        response = client.delete(f'/tasks/{last_id}')
        assert response.status_code == 200
        last_id_after_delete = get_last_task_row()['id']
        assert last_id is not last_id_after_delete
