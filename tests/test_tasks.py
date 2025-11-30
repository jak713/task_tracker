task = {"title": "Test Task",
                "description": "This is a test task.",
                "status": 0,
                "due_date_time": "2026-01-25T23:59",
                }

task_no_title = {"title": '',
                    "description": "This is a test task.",
                    "status": 0,
                    "due_date_time": "2026-01-25T23:59",}

task_empty_title = {"title": '     ',
                    "description": "This is a test task.",
                    "status": 0,
                    "due_date_time": "2026-01-25T23:59",}

task_invalid_datetime = {"title": "Test Task",
                    "description": "This is a test task.",
                    "status": 0,
                    "due_date_time": "25-01-2026",}

task_missing_due_date_time = {"title": "Test Task",
                    "description": "This is a test task.",
                    "status": 0,
                    "due_date_time": "",}

malicious_task = {"title": "Malicious Task'); DROP TABLE tasks;--",
            "description": "This task attempts SQL injection.",
            "status": 0,
            "due_date_time": "2026-01-25T23:59",}

special_char_task = {"title": "<Test>'\"Task",
            "description": "This task contains special characters: <>'\"",
            "status": 0,
            "due_date_time": "2026-01-25T23:59",}

class TestTaskCreation:
    """
    Testing POST / endpoint:
    1. Create task with expected data from HTML form
    2. Create task with expected data from JSON payload
    3. Create task with missing title
    4. Create task with empty title (whitespace only)§
    5. Create task with invalid datetime format
    6. Create task with missing due_date_time

    GET / endpoint:
    7. Retrieve all tasks from "/"
    """
    def test_create_task_html(self, client):
        response = client.post("/", data=task)

        assert response.status_code == 302
        assert b'Test Task' in client.get(response.headers['Location']).data
        assert b'This is a test task.' in client.get(response.headers['Location']).data
        assert b'incomplete' in client.get(response.headers['Location']).data
        assert b'2026-01-25 23:59' in client.get(response.headers['Location']).data
    
    def test_create_task_json(self, client):
        response = client.post("/", json=task)

        assert response.status_code == 201
        assert response.json['title'] == task['title']
        assert response.json['description'] == task['description']
        assert response.json['status'] == "incomplete" if task['status'] == 0 else "complete"
        assert response.json['due_date_time'] == task['due_date_time'].replace('T', ' ')

    def test_create_task_missing_title(self, client):
        response = client.post("/", json=task_no_title)

        assert response.status_code == 400
        assert "Title is required and cannot be empty." in response.json['error']

    def test_create_task_empty_title(self, client):
        response = client.post("/", json=task_empty_title)

        assert response.status_code == 400
        assert "Title is required and cannot be empty." in response.json['error']

    def test_create_task_invalid_datetime(self, client):
        response_json = client.post("/", json=task_invalid_datetime)
        response_web = client.post("/", data=task_invalid_datetime)

        assert response_json.status_code == 400
        assert "Invalid datetime format." in response_json.json['error']
        assert b'Invalid datetime format.' in response_web.data

    def test_create_task_missing_due_date_time(self, client):
        response_json = client.post("/", json=task_missing_due_date_time)
        response_web = client.post("/", data=task_missing_due_date_time)

        assert response_json.status_code == 400
        assert "Due date/time is required." in response_json.json['error']
        assert b'Due date/time is required.' in response_web.data

    def test_retrieve_all_tasks(self, client):
        # Assume tasks already exist
        response = client.get("/", headers={"Accept": "application/json"})
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) >= 0  

class TestTaskRetrieval:
    """
    Testing GET /<int:id> endpoint:
    1. Retrieve existing task by ID
    2. Retrieve non-existing task by ID
    """
    def test_retrieve_existing_task(self, client):
        # Create a task to retrieve
        create_response = client.post("/", json=task)
        task_id = create_response.json['id']

        # Retrieve the task
        retrieve_response = client.get(f"/{task_id}", headers={"Accept": "application/json"})

        assert retrieve_response.status_code == 200
        assert retrieve_response.json['title'] == task['title']
        assert retrieve_response.json['description'] == task['description']
        assert retrieve_response.json['status'] == "incomplete" if task['status'] == 0 else "complete"
        assert retrieve_response.json['due_date_time'] == task['due_date_time'].replace('T', ' ')

    def test_retrieve_non_existing_task(self, client):
        response_api = client.get("/99999", headers={"Accept": "application/json"})
        response_web = client.get("/99999")

        assert response_api.status_code == 404
        assert response_api.json['error'] == "Task not found."
        assert b'Task with ID 99999 not found.' in response_web.data

class TestTaskCompletion:
    """
    Testing POST /<int:id>/complete endpoint:
    1. Mark existing incomplete task as complete
    2. Mark existing complete task as complete (idempotent)
    3. Mark non-existing task as complete
    """
    ...

class TestTaskDeletion:
    """
    Testing POST /<int:id>/delete endpoint:
    1. Delete existing task by ID
    2. Delete non-existing task by ID
    """
    def test_delete_existing_task(self, client):
        # Create new task to obtain existing task ID
        create_response = client.post("/", json=task)
        task_id = create_response.json['id']
        print(task_id)
        response_api = client.post(f'/{task_id}/delete', headers={'Accept': 'application/json'})

        assert response_api.status_code == 200
        assert response_api.json['message'] == "Task deleted successfully."

    def test_delete_non_existing_task(self, client):
        response_api = client.post("/99999/delete", headers={"Accept": "application/json"})
        response_web = client.post("/99999/delete")

        assert response_api.status_code == 404
        assert response_api.json['error'] == "Task not found."
        assert b'You are trying to delete a task which does not exist!' in response_web.data

class TestSecurity:
    """
    Testing for common security vulnerabilities:
    1. SQL injection on task creation
    2. Special charracters handling (<>'")
    """
    def test_sql_injection_on_creation(self, client):
        response = client.post("/", json=malicious_task)

        assert response.status_code == 201
        assert response.json['title'] == malicious_task['title']

    def test_special_characters_handling(self, client):
        response = client.post("/", json=special_char_task)

        assert response.status_code == 201
        assert response.json['title'] == special_char_task['title']