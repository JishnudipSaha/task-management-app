from fastapi import Request, status, HTTPException, Depends
from sqlalchemy.orm import Session
from src.utils.settings import settings
from src.user.models import UserModel
from jwt.exceptions import InvalidTokenError
from src.utils.db import get_db
import jwt



# tokenized authentications of the user
def is_authenticated(request: Request, db: Session = Depends(get_db)):

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