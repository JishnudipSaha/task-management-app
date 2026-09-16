from this import d
from fastapi import APIRouter, Depends, status
from starlette.status import HTTP_201_CREATED
from src.user.dtos import UserSchema
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user import controller


user_routes = APIRouter(prefix='/user')


@user_routes.post('/register', status_code=HTTP_201_CREATED)
def register(body: UserSchema, db: Session = Depends(get_db)):
    return controller.register(body = body, db = db)