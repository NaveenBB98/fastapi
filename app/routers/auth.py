from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import database
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from .. import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentials')
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentials')
    oauth_token=oauth2.create_access_token(data={'userid':user.id})
    return {"token":oauth_token,"token_type":"bearer"}

    

