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
