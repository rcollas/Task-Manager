from core.db import (get_db)


def get_last_task_row():
    db = get_db()
    task = db.execute("SELECT * FROM task ORDER BY id desc limit 1").fetchone()
    return task
