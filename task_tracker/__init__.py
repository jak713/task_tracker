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

    @app.route('/')
    def main():
        return redirect('/tasks')

    from . import db
    db.init_app(app)
    
    from . import tasks
    app.register_blueprint(tasks.bp)

    app.add_url_rule('/tasks', endpoint='tasks', view_func=tasks.tasks, methods=['GET', 'POST'])

    app.add_url_rule('/tasks/<int:id>', endpoint='confirmation', view_func=tasks.confirmation, methods=['GET'])

    app.add_url_rule('/tasks/<int:id>/delete', endpoint='delete_task', view_func=tasks.delete_task, methods=['POST','GET'])
    
    app.add_url_rule('/tasks/<int:id>/complete', endpoint='complete_task', view_func=tasks.complete_task, methods=['POST','GET'])
    
    return app
