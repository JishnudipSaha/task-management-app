from pydantic import BaseModel


class UserSchema(BaseModel):
    name : str
    user_name : str
    password : str
    email : str