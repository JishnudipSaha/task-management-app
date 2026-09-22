from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException, status
from src.user.models import UserModel

def create_task(body: TaskSchema, db: Session, user: UserModel):
    data = body.model_dump()
    new_task = TaskModel(title = data["title"], 
                            description = data["description"],
                            is_completed = data["is_completed"],
                            user_id = user.id)
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task
    
    
def get_tasks(db: Session, user: UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    
    # cheking if the user does not created any tasks
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have not created any task')

    return tasks
    
def get_one_task(task_id: int, db: Session, user: UserModel):
    one_task = db.query(TaskModel).get(task_id)

    # checking if the task exists in the db or not
    if not one_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task NOT FOUND")
    
    # checking if the task belongs to the authorized user
    if one_task.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are UNAUTHORIZED")
    
    return one_task
    
    
def update_task(body: TaskSchema, task_id: int, db: Session, user: UserModel):
    one_task = db.query(TaskModel).get(task_id)

    # checking if the task exists in the db or not
    if not one_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task NOT FOUND")
    
    # checking if the task are being updated by the registered user or not
    if one_task.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are UNAUTHORIZED")

    body = body.model_dump()
    for field, value in body.items():
        setattr(one_task, field, value)
    
    db.add(one_task)
    db.commit()
    db.refresh(one_task)
    
    return one_task
    
    
def delete_task(task_id: int, db: Session, user: UserModel):
    one_task = db.query(TaskModel).get(task_id)
    # checking if the task exists in the db or not
    if not one_task:
        raise HTTPException(404, detail="Task id is incorrect.")
    
    # checking if the task is being deleted by the authorized user or not
    if one_task.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are UNAUTHORIZED')

    db.delete(one_task)
    db.commit()
    
    return None