from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import schema,models,jwt_token
from .. import database
from . import user
from fastapi.security import OAuth2PasswordRequestForm
router=APIRouter(
    tags=['Authentication']
)

def verify(plain_password,hashed_password):
    
    return user.pwd_context.verify(plain_password,hashed_password)


@router.post('/login')

def login(req:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==req.username).first()
    if not user:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"invalid user name")
    if not verify(req.password,user.password):
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"incorrect password")
    
    access_token = jwt_token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token":access_token, "token_type":"bearer"}
