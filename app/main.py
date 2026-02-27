from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  #for asynchronous database sessions
from contextlib import asynccontextmanager  #for managinf the lifespan of the application
from sqlalchemy import select



from .database import get_async_session,create_db_and_tables  #importing database connection and table creation function
from .models import Todo,user
from .schemas import todolist,todo_update,user_create,user_login
from .auth_utils import hash_password,verify_password,create_access_token,get_current_user
from fastapi.security import OAuth2PasswordRequestForm

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

app=FastAPI(lifespan=lifespan)



@app.post("/add")
async def post_todos(
        todo:todolist,
        session:AsyncSession=Depends(get_async_session),
        user_id:str=Depends(get_current_user)
    ):
    print("fuser id in post_todos:", user_id) 
    new_todo = Todo(
        title=todo.title,
        completed=todo.completed,
        owner_id=user_id  
    )
    session.add(new_todo)
    await session.commit()
    return{"message":"todo added successfully"}



@app.get("/todos")
async def get_my_todos(
    session: AsyncSession = Depends(get_async_session),
    user_id: str = Depends(get_current_user)
):
    statement = select(Todo).where(Todo.owner_id == user_id)
    result = await session.execute(statement)
    todos = result.scalars().all()
    
    return todos
    
    

@app.put("/update/{todo_id}")
async def update_todo(
    todo_id:str,
    todo_data:todo_update,
    session:AsyncSession=Depends(get_async_session),
    user_id:str=Depends(get_current_user)
):
    result=await session.execute(select(Todo).where(Todo.id==todo_id,Todo.owner_id==user_id))
    todo=result.scalar_one_or_none()
    if not todo:
        raise HTTPException(status_code=404,detail="todo not found")
    todo.completed=not todo.completed

    if todo_data.title is not None:
        todo.title=todo_data.title

    if todo_data.completed is not None:
        todo.completed=todo_data.completed
    
    session.add(todo)

    await session.commit()
    await session.refresh(todo)
    return{
        "id":todo.id,
        "title":todo.title,
        "completed":todo.completed
    }
    
@app.delete('/delete/{todo_id}')
async def delete_todo(
    todo_id: str,
    session: AsyncSession = Depends(get_async_session),
    user_id: str = Depends(get_current_user)  
):
    
    result = await session.execute(
        select(Todo).where(Todo.id == todo_id, Todo.owner_id == user_id)
    )
    todo = result.scalar_one_or_none()
    
    if not todo:
        
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized")

    await session.delete(todo)
    await session.commit()
    return {"message": "Todo deleted successfully"}
    
# user authentication
@app.post("/signup")
async def signup(
    user_data:user_create,session:AsyncSession=Depends(get_async_session)
):
    hashed=hash_password(user_data.password)
    new_user=user(email=user_data.email,password=hashed)
    session.add(new_user)
    await session.commit()
    return{"message":"data added successfully"}

from fastapi.security import OAuth2PasswordRequestForm

@app.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(user).where(user.email == form_data.username))
    db_user = result.scalar_one_or_none()
    
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}