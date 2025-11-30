A task management API built for HMCTS's Junior SWE coding task.

API endpoints:
- `POST /`: Create a new task
- `GET /`: List all tasks
- `GET /<id>`: Retrieve task details (e.g. when confirming creation)
- `POST /<id>/complete`: Mark a task as completed
- `POST /<id>/delete`: Remove a task

The technical criteria and how I have approached them: 
- Backend: Python with Flask
- Frontend: Simple HTML/CSS, with the caveat that HTML forms can only do GET and POST requests natively. I wanted to keep it simple and avoid adding JavaScript for this assessment.
- Implement unit tests --> pytest is used for this with tests located in the `tests` directory.
- Store data in a database --> sqlite (raw SQL) over an ORM only to again keep things simpler.
- Include validation and error handling --> 
- Document API endpoints --> See above.

## How to run the application
1. Clone the repository
2. Navigate to the `task-tracker` directory
3. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Initialise the database:
   ```bash
   flask --app task_tracker init-db
   ```
5. Run the Flask application:
   ```bash
   flask --app task_tracker run --debug
   ```  
6. Head to localhost (http://127.0.0.1:5000)

The Scenario/Task:

```HMCTS requires a new system to be developed so caseworkers can keep track of their tasks.

Your technical test is to develop a new system to facilitate the creation of these tasks.

Task Requirements
You are required to create a backend API that allows for the creation of new tasks, and a frontend application to interact with this.

A task should have the following properties:

Title
Description (optional field)
Status
Due date/time
On successful task creation, the API should return the task and the frontend display a confirmation message alongside the successfully created task details.

No other CRUD operations related to the management of tasks are required.
```