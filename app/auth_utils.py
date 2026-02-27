from datetime import datetime,timedelta,timezone
# libraries for JWT handling
from jose import jwt,JWTError

# libraries for password hashing and token generation

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

import os
from dotenv import load_dotenv

# .env file load karne ke liye
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# password hashing using bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
       
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
        
        return user_id 
    except JWTError:
        raise credentials_exception
    

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password:str,hashed_password:str):
    return pwd_context.verify(password,hashed_password)

def create_access_token(data:dict,expires_delta:timedelta|None=None):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+(expires_delta or timedelta(minutes=15))
    to_encode.update({"exp":expire}) 
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    