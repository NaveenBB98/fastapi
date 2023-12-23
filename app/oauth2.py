from datetime import datetime, timedelta
from fastapi import Response, status, HTTPException, Depends
from jose import JWTError,jwt
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from . import database,models
from sqlalchemy.orm import Session
from .config import settings

oauth2scheme=OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get('userid')
        id=str(id)
        if id is None:
            return credentials_exception
        token_data=schemas.TokenData(id=id)
    except JWTError as e:
        raise credentials_exception
    except AssertionError as e:
        print(e)
    return token_data

def get_current_user(token:str=Depends(oauth2scheme),db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",headers={'WWW-Authenticate':'Bearer'})
    token_data=verify_access_token(token,credentials_exception)
    
    user=db.query(models.User).filter(models.User.id == token_data.id).first()
    return user





