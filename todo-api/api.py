from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Create API instance
api = Api(app)

# Set database URI for SQLAlchemy (using SQLite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Define database model for the ToDo items
class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each task
    task = db.Column(db.String(200))  # The actual task to be completed
    summary = db.Column(db.String(500))  # Additional details about the task

# Create database within the application context
with app.app_context():
    db.create_all()  # Create the tables in the database

# Predefined tasks (used for testing purposes)
todos = {
    1: {"task": "Hello World Program 1", "summary": "Hello World Summary 1"},
    2: {"task": "Hello World Program 2", "summary": "Hello World Summary 2"}
}

# Argument parser for POST request (requires 'task' and 'summary' fields)
task_post_args = reqparse.RequestParser()
task_post_args.add_argument("task", type=str, help="Task is required", required=True)
task_post_args.add_argument("summary", type=str, help="Summary is required", required=True)

# Argument parser for PUT request (optional 'task' and 'summary' fields)
task_update_args = reqparse.RequestParser()
task_update_args.add_argument("task", type=str)
task_update_args.add_argument("summary", type=str)

# Define how the resource fields should be serialized
resource_fields = {
    'id': fields.Integer,
    'task': fields.String,
    'summary': fields.String
}

# Resource for listing all tasks
class ToDoList(Resource):
    def get(self):
        # Retrieve all tasks from the database
        tasks = ToDoModel.query.all()
        todos = {}
        for task in tasks:
            todos[task.id] = {"task": task.task, "summary": task.summary}
        return todos

# Resource for interacting with a specific task
class ToDo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        # Retrieve a specific task by its ID
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message='Could not find task')
        return task

    @marshal_with(resource_fields)
    def post(self, todo_id):
        # Add a new task
        args = task_post_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(409, message='Task ID already taken')

        todo = ToDoModel(id=todo_id, task=args['task'], summary=args['summary'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201

    @marshal_with(resource_fields)
    def put(self, todo_id):
        # Update an existing task
        args = task_update_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message="Task does not exist! Cannot update.")
        if args['task']:
            task.task = args['task']
        if args['summary']:
            task.summary = args['summary']
        db.session.commit()
        return task

    def delete(self, todo_id):
        # Delete a task
        task = ToDoModel.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        db.session.commit()
        return 'Todo Deleted', 204

# Add the resources to the API
api.add_resource(ToDo, '/todo/<int:todo_id>')
api.add_resource(ToDoList, '/todos')

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
