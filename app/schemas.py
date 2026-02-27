from pydantic import BaseModel
from typing import Optional

class todolist(BaseModel):
    title:str
    completed:bool=False

class todo_update(BaseModel):
    title:Optional[str]=None    
    completed: Optional[bool] = None

class user_create(BaseModel):
    email:str
    password:str

class user_login(BaseModel):
    email:str
    password:str
