from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form
from contextlib import asynccontextmanager
import httpx

from .db import init_db
from .schemas import Task, TaskCreate, TaskUpdate
from .crud import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task
)

API_BASE_URL = "http://127.0.0.1:8000/api"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="To-Do API",
    version="1.0.0",
    lifespan=lifespan
)

templates = Jinja2Templates(directory="app/templates")


@app.get("/api/tasks", tags=["Tasks API"],
         response_model=list[Task], )
def api_list_tasks():
    return get_tasks()


@app.post("/api/tasks", tags=["Tasks API"],
          response_model=dict, )
def api_create_task(task: TaskCreate):
    task_id = create_task(task)
    return {"id": task_id, "message": "Task created"}


@app.get("/api/tasks/{task_id}",
         tags=["Tasks API"],
         response_model=Task, )
def api_get_task(task_id: int):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/api/tasks/{task_id}", tags=["Tasks API"],response_model=dict )
def api_update_task(task_id: int, task: TaskUpdate):
    updated = update_task(task_id, task.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated"}


@app.delete("/api/tasks/{task_id}", tags=["Tasks API"], response_model=dict )
def api_delete_task(task_id: int):
    deleted = delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def web_list(request: Request):
    with httpx.Client() as client:
        response = client.get(f"{API_BASE_URL}/tasks")
        tasks = response.json()

    return templates.TemplateResponse(
        "list.html",
        {"request": request, "tasks": tasks}
    )


@app.get("/create", response_class=HTMLResponse, include_in_schema=False)
def create_task_form(request: Request):
    return templates.TemplateResponse(
        "create.html",
        {"request": request}
    )


@app.post("/create", include_in_schema=False)
def create_task_submit(
        title: str = Form(...),
        description: str = Form("")
):
    payload = {
        "title": title,
        "description": description
    }

    with httpx.Client() as client:
        client.post(f"{API_BASE_URL}/tasks", json=payload)

    return RedirectResponse("/", status_code=303)


@app.get("/edit/{task_id}", response_class=HTMLResponse, include_in_schema=False)
def edit_task_form(task_id: int, request: Request):
    with httpx.Client() as client:
        response = client.get(f"{API_BASE_URL}/tasks/{task_id}")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Task not found")

    task = response.json()

    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "task": task}
    )


@app.post("/edit/{task_id}", include_in_schema=False)
def edit_task_submit(
        task_id: int,
        title: str = Form(...),
        description: str = Form(""),
        status: str = Form("pending")
):
    payload = {
        "title": title,
        "description": description,
        "status": status
    }

    with httpx.Client() as client:
        response = client.put(
            f"{API_BASE_URL}/tasks/{task_id}",
            json=payload
        )

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Task not found")

    return RedirectResponse("/", status_code=303)


@app.post("/delete/{task_id}", include_in_schema=False)
def delete_task_ui(task_id: int):
    with httpx.Client() as client:
        client.delete(f"{API_BASE_URL}/tasks/{task_id}")

    return RedirectResponse("/", status_code=303)
