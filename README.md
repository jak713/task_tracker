A task management CRUD application built for HMCTS's Junior SWE technical assessment. 

API endpoints:
- `POST /tasks`: Create a new task
- `GET /tasks/<id>`: Retrieve task details (e.g. when confirming creation)
- `POST /tasks/<id>/complete`: Mark a task as completed
- `POST /tasks/<id>/delete`: Remove a task

The technical criteria and how I have approached them: 
- Backend: Python with Flask
- Frontend: Simple HTML/CSS, with the caveat that HTML forms can only do GET and POST requests natively.
- Implement unit tests --> pytest and pytest-flask
- Store data in a database --> sqlite
- Include validation and error handling --> Validation for required fields, error handling for invalid data formats.
- Document API endpoints --> See above.

Some added features:
- Task creation, completion, and deletion
- Colour-coding for deadline tracking (orange = approaching, red = overdue)

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
   flask init-db
   ```
5. Run the Flask application:
   ```bash
   flask run
   ```  

The Scenario/Task is verbatim:

`HMCTS requires a new system to be developed so caseworkers can keep track of their tasks.

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
`