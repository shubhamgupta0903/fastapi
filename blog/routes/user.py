from fastapi import APIRouter,HTTPException,Depends,status
from .. import models,schema
from sqlalchemy.orm import Session
from .. import database
from passlib.context import CryptContext

get_db=database.get_db

router =APIRouter(
    tags=['User'],
    prefix='/user'
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/")

def create_user(request:schema.user,db:Session=Depends(get_db)):
    hashed_pwd=pwd_context.hash(request.password)
    new_user=models.User(name=request.name,email=request.email,password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schema.show_user)

def get_user(id:int,db:Session=Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} is not available")
    return user