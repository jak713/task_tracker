from datetime import datetime
from .db import get_db
from flask import render_template, request, redirect, Blueprint, jsonify, Response
import json

bp = Blueprint('tasks', __name__, url_prefix='/tasks')
# CRUD = Create, Read, Update, Delete

def refresh() -> list:
    db = get_db()
    # Retrieve tasks as list of dictionaries
    tasks = db.execute('SELECT * FROM tasks').fetchall()
    return tasks

def validate_task_input(title, due_date_time) -> list:
    errors = []

    if not title or not title.strip():
        errors.append("Title is required and cannot be empty.")

    if not due_date_time:
        errors.append("Due date/time is required.")
    else:
        try:
            datetime.fromisoformat(due_date_time.replace('T', ' '))
        except ValueError:
            errors.append("Invalid datetime format.")

    return errors

def task_to_dict(task) -> dict:
    """Convert database row to dictionary.
        Returns dict of task."""
    return {
        'id': task['id'],
        'title': task['title'],
        'description': task['description'],
        'status': 'complete' if task['status'] == 1 else 'incomplete',
        'due_date_time': task['due_date_time']  
    }

# Create 
@bp.route('', methods=['POST'])
def create_task():
        if request.is_json:
            data = request.get_json()
            title = data.get('title', '').strip()
            description = data.get('description', '').strip() if data.get('description') else None
            status = data.get('status', 0)
            due_date_time = data.get('due_date_time', '')
        else:
            # If request from web form
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip() if request.form.get('description') else None
            status = request.form.get('status', 0)
            due_date_time = request.form.get('due_date_time', '')

        errors = validate_task_input(title, due_date_time)
        if errors:
            if request.is_json: 
                # Return bad request with errors in JSON
                return jsonify({'error': "; ".join(errors)}), 400
            else:
                return render_template('base.html', tasks=refresh(), message="; ".join(errors))
            
        due_date_time = due_date_time.replace('T', ' ')
        try:
            db = get_db()
            db.execute(
                'INSERT INTO tasks (title, description, status, due_date_time) VALUES (?, ?, ?, ?)',
                (title, description, status, due_date_time)
            )
            db.commit()

            task_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
            task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

            if request.is_json:
                # Return created 
                return jsonify(task_to_dict(task)), 201
            else:
                return redirect(f'/tasks/{task_id}')
            
        except Exception:
            if request.is_json:
                return jsonify({'error': "Database error occurred."}), 500
            else:
                return render_template('base.html', tasks=refresh(), message="An error occurred while creating the task.")

# Read
@bp.route('', methods=['GET'])
def tasks():
    if request.accept_mimetypes.best == 'application/json':
        # If API request, return OK JSON list of tasks
        tasks = refresh()
        tasks_list = [task_to_dict(task) for task in tasks]
        return Response(json.dumps(tasks_list), mimetype='application/json'), 200
    else:
        # If web request, retrieve updated list of tasks and update the frontend
        return render_template('base.html', tasks=refresh())

# Read 
@bp.route('/<int:id>', methods=['GET'])
def get_task(id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()

    if not task:
        if request.accept_mimetypes.best == 'application/json':
            return jsonify({'error': 'Task not found.'}), 404
        else:
            return render_template('base.html', tasks=refresh(), message=f"Task with ID {id} not found.")
    
    if request.accept_mimetypes.best == 'application/json':
        return jsonify(task_to_dict(task)), 200
    else:
        return render_template('base.html', task=task, tasks=refresh())

# Update
@bp.route('/<int:id>/complete', methods=['POST'])
def complete_task(id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()

    if not task:
        if request.is_json or request.accept_mimetypes.best == 'application/json':
            # Return not found
            return jsonify({'error': 'Task not found.'}), 404
        else:
            return render_template('base.html', tasks=refresh(), message="You are trying to complete a task which does not exist!")
    
    if task['status'] == 1:
        if request.is_json or request.accept_mimetypes.best == 'application/json':
            return jsonify({'error': 'Task is already complete.'}), 400
        else:
            return render_template('base.html', tasks=refresh(), message="This task is already marked as complete!")
    
    db.execute('UPDATE tasks SET status = 1 WHERE id = ?', (id,))
    db.commit()

    updated_task = db.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    # Return updated task as JSON
    if request.is_json or request.accept_mimetypes.best == 'application/json':
        return jsonify(task_to_dict(updated_task)), 200
    else:
        return render_template('base.html', tasks=refresh())

# Delete
@bp.route('/<int:id>/delete', methods=['POST'])
def delete_task(id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
        
    if not task:
        if request.is_json or request.accept_mimetypes.best == 'application/json':
            return jsonify({'error': 'Task not found.'}), 404
        else:
            return render_template('base.html', tasks=refresh(), message="You are trying to delete a task which does not exist!")
        
    db.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()

    if request.is_json or request.accept_mimetypes.best == 'application/json':
        return jsonify({'message': 'Task deleted successfully.'}), 200
    else:
        return render_template('base.html', tasks=refresh())
