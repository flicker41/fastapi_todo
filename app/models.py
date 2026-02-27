from sqlalchemy import Column, String, Boolean,ForeignKey
from .database import Base
import uuid

class Todo(Base):
    __tablename__ = "todosapp"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    owner_id =Column(String,ForeignKey("users.id"),nullable=False)

class user(Base):
    __tablename__="users"

    id=Column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
