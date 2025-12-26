from django.db import connection

def create_tasks_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)

def dict_fetch_all(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def create_task(data):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO tasks (title, description, due_date, status)
            VALUES (%s, %s, %s, %s)
            """,
            [
                data['title'],
                data.get('description'),
                data.get('due_date'),
                data.get('status', 'pending')
            ]
        )
        return cursor.lastrowid


def get_all_tasks():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks")
        return dict_fetch_all(cursor)


def get_task(task_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks WHERE id=%s", [task_id])
        row = cursor.fetchone()
        if not row:
            return None
        return dict(zip([c[0] for c in cursor.description], row))


def update_task(task_id, data):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE tasks
            SET title=%s, description=%s, due_date=%s, status=%s
            WHERE id=%s
            """,
            [
                data['title'],
                data.get('description'),
                data.get('due_date'),
                data.get('status'),
                task_id
            ]
        )


def delete_task(task_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM tasks WHERE id=%s", [task_id])