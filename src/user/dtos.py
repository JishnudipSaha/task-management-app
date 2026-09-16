from pydantic import BaseModel


class UserSchema(BaseModel):
    name : str
    user_name : str
    password : str
    email : str

class UserResponseSchema(BaseModel):
    id : int
    name : str
    user_name : str
    email : str