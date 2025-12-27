from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: str = "pending"

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Demo title",
                "description": "The description of tasks",
                "due_date": "2025-01-01",
                "status": "pending"
            }
        }
    }

class Task(TaskCreate):
    id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Demo title",
                "description": "The description of tasks",
                "due_date": "2025-01-01",
                "status": "pending"
            }
        }
    }


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Demo Title",
                "description": "The description of tasks",
                "due_date": "2025-01-01",
                "status": "done"
            }
        }
    }


