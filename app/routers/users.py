from .. import models,utils,schemas
from http.client import HTTPException
from fastapi import HTTPException,Depends,APIRouter
from ..database import engine,get_db,sessionLocal
from sqlalchemy.orm import Session
#from typing import List

router = APIRouter(
    prefix='/user',
    tags = ['Users']
)

@router.post('/',status_code=201, response_model=schemas.UserResponse)
def create_user(user : schemas.UserCreate, db:Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model = schemas.UserResponse)
def getuser(id:int , db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= 404, detail=f'User not found for {id}')
    return user
