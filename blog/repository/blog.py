from fastapi import Depends
from .. import models
from sqlalchemy.orm import Session


def all(db:Session):
    blogs=db.query(models.Blog).all()
    return blogs