from fastapi import HTTPException, status, Request
from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError


password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def register(body: UserSchema, db: Session):
    '''1. User validation'''
    is_user = db.query(UserModel).filter(UserModel.user_name == body.user_name).first()
    if is_user:
        raise HTTPException(status_code=400, detail='Username already exists')

    '''2. Email validation'''
    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_email:
        raise HTTPException(status_code=400, detail='Email address already exists')

    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        user_name = body.user_name,
        hash_password = hash_password,
        email = body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(body: LoginSchema, db:Session):

    user = db.query(UserModel).filter(UserModel.user_name == body.user_name).first()

    # if the username is wrong
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Entered wrong username')

    # if the password is wrong
    if not verify_password(plain_password=body.password, hashed_password=user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Entered wrong password')
    
    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)

    token = jwt.encode({"_id" : user.id, "exp": exp_time.timestamp()}, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return{
        "token": token
    }


def is_authenticated(request: Request, db: Session):

    try:
        token = request.headers.get('authorization')

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            
        token = token.split(" ")[-1]
        data = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id = data.get('_id')

        # checking if the user existes in the db or not.
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Entered wrong username')

        # return the user.
        return user
        
    except InvalidTokenError:
        # if the token validation reise error then rasie this http exception
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')