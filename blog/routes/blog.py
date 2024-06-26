from fastapi import APIRouter,Depends,HTTPException,status
from .. import models
from .. import database
from sqlalchemy.orm import Session
from .. import schema
from ..repository import blog
from ..Oauth2 import get_current_user


get_db=database.get_db

router=APIRouter(
    tags=['Blogs'],
    prefix='/blog'
)

@router.get("/all")
def all(db:Session=Depends(get_db),get_current_user:schema.user=Depends(get_current_user)):
    return blog.all(db)

@router.post("/")
def create(request:schema.Blog,db:Session =Depends(get_db),get_current_user:schema.user=Depends(get_current_user)):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete("/{id}")
def destroy(id,db:Session =Depends(get_db),get_current_user:schema.user=Depends(get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return "done"

@router.put("/{id}")
def update(request:schema.Blog,id,db:Session =Depends(get_db),get_current_user:schema.user=Depends(get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    blog.title=request.title
    blog.body=request.body
    
    db.commit()
    db.refresh(blog)
    return blog

@router.get("/{id}",response_model=schema.show_blog)

def show(id,db:Session=Depends(get_db),get_current_user:schema.user=Depends(get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    return blog
