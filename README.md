# To-Do List Application (FastAPI)

![Tests](https://github.com/psychoAKASH/todo_task/actions/workflows/tests.yml/badge.svg)


A To-Do List web application built using **FastAPI** and **SQLite**, providing
RESTful APIs for task management along with a minimal UI rendered using templates.

The project demonstrates clean API design, database handling without ORM.

---

##  Features

- Create, read, update, and delete tasks (CRUD)
- RESTful APIs with proper request/response schemas
- Swagger API documentation with examples
- UI built using server-side templates
- SQLite database (no ORM used)
- Automated unit tests using pytest
- GitHub Actions CI for running tests
- Dockerized setup for easy spin-up

---

##  Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite
- **Templating:** Jinja2
- **Testing:** pytest
- **CI/CD:** GitHub Actions
- **Containerization:** Docker

---

## Project Structure
```markdown
todo_task/
├── app/
│ ├── main.py
│ ├── crud.py
│ ├── db.py 
│ ├── schemas.py 
│ ├── templates/
│ └── tests/
├── .github/workflows/ 
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
---

##  API Documentation

Once the application is running, Swagger documentation is available at:
http://127.0.0.1:8000/docs

- Only **API endpoints** are documented
- UI routes are excluded from Swagger
- Each API includes request/response schemas and example payloads

---

##  Running Tests

Tests are written using `pytest` and use an isolated temporary SQLite database.

### Run tests locally:
```bash
pytest
```
- All tests run automatically on every push and pull request via GitHub Actions.

---
## Running the Application (Local)
### Create virtual environment
```bash
python -m venv venv
````
then 
```bash
source venv/bin/activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Start the server
```bash
uvicorn app.main:app --reload
```

---

## Running with Docker
Build and run the container:
``` bash
docker compose up --build
```

This will:

- Start the FastAPI application

- Initialize the SQLite database automatically

---

## API Endpoints

### All API endpoints are prefixed with `/api` and documented via Swagger.

| Method | Endpoint               | Description            |
|------|------------------------|------------------------|
| POST | `/api/tasks`           | Create a new task      |
| GET  | `/api/tasks`           | Get all tasks          |
| GET  | `/api/tasks/{id}`      | Get task by ID         |
| PUT  | `/api/tasks/{id}`      | Update a task          |
| DELETE | `/api/tasks/{id}`    | Delete a task          |

---

##  Design Decisions

- No ORM used: Raw SQL is used to demonstrate database fundamentals
- API-first approach: UI communicates with the backend only via APIs
- Separation of concerns: API routes and UI routes are clearly separated
- Test isolation: Each test run uses a temporary database

---

## Improvements and suggestions

- Adding user authentication
- Interacting with db asynchronously
- Adding pagination for tasks
- Replacing sqlite3 with any other db like postgresql
- Refactoring the api routes into the routers.


