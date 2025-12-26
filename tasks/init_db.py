import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo_project.settings")
django.setup()

from tasks.db import create_tasks_table

if __name__ == "__main__":
    create_tasks_table()
    print("Database initialized")