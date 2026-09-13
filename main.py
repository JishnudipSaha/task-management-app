from fastapi import FastAPI
from src.utils.db import Base, engine
from src.tasks.models import TaskModel
from src.tasks.router import task_routes


Base.metadata.create_all(engine)



app = FastAPI(title='This is a task management application')
app.include_router(task_routes)



@app.get('/')
def home():
    return {
        'status': 'Welcome to home Jishnudip'
    }