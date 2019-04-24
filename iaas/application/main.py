from typing import List
import subprocess

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_204_NO_CONTENT

# Database Handling

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@127.0.0.1/tododb?charset=utf8'

database = databases.Database(SQLALCHEMY_DATABASE_URI)

metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("item", sqlalchemy.String),
    sqlalchemy.Column("is_done", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URI
)
metadata.create_all(engine)

# Model

class TaskItemOnly(BaseModel):
    item: str

class TaskWithoutId(BaseModel):
    item: str
    is_done: bool

class Task(BaseModel):
    id: int
    item: str
    is_done: bool

# Controller

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/initialize")
async def init_db():
    res = subprocess.call('./init.sh')
    if res == 0:
        return "OK"
    else:
        return "NG", 500
    return None


@app.get("/tasks", response_model=List[Task])
async def read_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    query = "SELECT * FROM tasks WHERE id = :task_id"
    task = await database.fetch_one(query=query, values={"task_id": task_id})
    if task is None:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND)
    else:
        return task


@app.post("/tasks", response_model=Task)
async def create_task(task: TaskItemOnly):
    query = tasks.insert().values(item=task.item, is_done=False)
    last_record_id = await database.execute(query)
    return {"id": last_record_id, "item": task.item, "is_done": False}


@app.put("/tasks/{task_id}", response_model=Task)
async def modify_task(task_id: int, task: TaskWithoutId):
    query = "UPDATE tasks SET item = :task_item, is_done = :task_is_done WHERE id = :task_id"
    await database.execute(query=query, values={"task_id": task_id, "task_is_done": task.is_done, "task_item": task.item})
    return {"id": task_id, "item": task.item, "is_done": False}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    query = "DELETE FROM tasks WHERE id = :task_id"
    await database.execute(query=query, values={"task_id": task_id})
    return JSONResponse(status_code=HTTP_204_NO_CONTENT)
