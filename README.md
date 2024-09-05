# Flask ToDo REST API

This project implements a simple RESTful API using Flask, Flask-RESTful, and Flask-SQLAlchemy. It allows users to create, retrieve, update, and delete tasks from a SQLite database.

## Features

- **GET** `/todos`: Retrieve all tasks.
- **GET** `/todo/<id>`: Retrieve a specific task by ID.
- **POST** `/todo/<id>`: Create a new task with a unique ID.
- **PUT** `/todo/<id>`: Update an existing task.
- **DELETE** `/todo/<id>`: Delete a task by ID.

## Requirements

- Python 3.x
- Flask
- Flask-RESTful
- Flask-SQLAlchemy

## Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/Flask-Todo-API.git](https://github.com/akhilk27/Flask-ToDo-API.git
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python api.py
```


## Usage

Use any API client like Postman or curl to interact with the API.

Example: Create a new task

curl -X POST http://127.0.0.1:5000/todo/1 -d "task=New Task" -d "summary=New Summary"

Example: Retrieve all tasks

curl http://127.0.0.1:5000/todos

