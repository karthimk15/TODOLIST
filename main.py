from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sqlite3
#------FastAPI instance-------
app = FastAPI()
#allow React (localhost:5173))
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("tasks.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS tasks(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          task TEXT NOT NULL)""")
#----------PYDANTIC MODEL FOR POST----------
class Task(BaseModel):
    task : str
@app.get("/tasks")
def get_tasks():
    rows = c.execute("SELECT * FROM tasks")
    return [dict(row) for row in rows]

@app.post("/task")
def create_task(task: Task):
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task.task,))
    conn.commit()
    return {"message": f"Task '{task.task}' added successfully"}
@app.delete("/task/{task_id}")
def delete_task(task_id: int):
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    return {"message": f"Task {task_id} deleted successfully"}
