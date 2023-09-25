import pytest
from core.db import (get_db)


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
        task = db.execute("SELECT * FROM task ORDER BY id desc limit 1").fetchone()
        assert task['title'] == title
        assert task['description'] == description

