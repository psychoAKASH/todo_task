import os
import tempfile


temp_db = tempfile.NamedTemporaryFile(delete=False)
os.environ["TASK_DB_PATH"] = temp_db.name

import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.db import init_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield


def test_create_task():
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task"}
    )
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_tasks():
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_task():
    create_res = client.post(
        "/api/tasks",
        json={"title": "Single Task"}
    )
    task_id = create_res.json()["id"]

    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Single Task"


def test_update_task():
    create_res = client.post(
        "/api/tasks",
        json={"title": "Old Title"}
    )
    task_id = create_res.json()["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated Title"}
    )
    assert response.status_code == 200

    get_res = client.get(f"/api/tasks/{task_id}")
    assert get_res.json()["title"] == "Updated Title"


def test_delete_task():
    create_res = client.post(
        "/api/tasks",
        json={"title": "To be deleted"}
    )
    task_id = create_res.json()["id"]

    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 200

    get_res = client.get(f"/api/tasks/{task_id}")
    assert get_res.status_code == 404


def test_task_not_found():
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404