import os
from flask import Flask,redirect

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Override secret_key to a random value when deploying
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'task_tracker.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    
    from . import tasks
    app.register_blueprint(tasks.bp)

    # Create
    app.add_url_rule('/', endpoint='', view_func=tasks.create_task, methods=['POST'])
    # Read
    app.add_url_rule('/', endpoint='tasks', view_func=tasks.tasks, methods=['GET'])
    app.add_url_rule('/<int:id>', endpoint='get_task', view_func=tasks.get_task, methods=['GET'])
    # Update
    app.add_url_rule('/<int:id>/complete', endpoint='complete_task', view_func=tasks.complete_task, methods=['POST','GET'])
    # Delete
    app.add_url_rule('/<int:id>/delete', endpoint='delete_task', view_func=tasks.delete_task, methods=['POST','GET'])
    
    return app
