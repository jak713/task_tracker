from .db import get_db
from flask import render_template, request, redirect, Blueprint

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def refresh():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks').fetchall()
    return tasks


@bp.route('/tasks', methods=['POST', 'GET'])
def tasks():
    if request.method == 'POST':
        title = sanitise_input(request.form['title'])
        description = sanitise_input(request.form['description'])
        status = sanitise_input(request.form['status'])
        due_date_time = sanitise_input(request.form['due_date_time'].replace('T', ' ')) # since YYYY-MM-DDTHH:MM format from input
        db = get_db()
        db.execute(
            'INSERT INTO tasks (title, description, status, due_date_time) VALUES (?, ?, ?, ?)',
            (title, description, status, due_date_time)
        )
        db.commit()
        return redirect(f'/tasks/{db.execute("SELECT last_insert_rowid()").fetchone()[0]}')
    # Retrieve updated list of tasks (for GET)
    return render_template('base.html', tasks=refresh())

@bp.route('/tasks/<int:id>/delete', methods=['POST', 'GET'])
def delete_task(id):
    # if given ID does not exist, no action is taken
    if not get_db().execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone():
        return render_template('base.html', tasks=refresh(), message="You are trying to delete a task, which does not exist!")
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()
    return render_template('base.html', tasks=refresh())

@bp.route('/tasks/<int:id>/complete', methods=['POST', 'GET'])
def complete_task(id):
    if not get_db().execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone():
        return render_template('base.html', tasks=refresh(), message="You are trying to complete a task, which does not exist!")
    
    if get_db().execute('SELECT * FROM tasks WHERE id = ? AND status = 1', (id,)).fetchone():
        return render_template('base.html', tasks=refresh(), message="This task is already marked as complete!")
    
    db = get_db()
    db.execute('UPDATE tasks SET status = 1 WHERE id = ?', (id,))
    db.commit()
    return render_template('base.html', tasks=refresh())

@bp.route('/tasks/<int:id>', methods=['GET'])
def confirmation(id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    return render_template('base.html', task=task, tasks=refresh())

# Security functions

def sanitise_input(input_str):
    return input_str.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')