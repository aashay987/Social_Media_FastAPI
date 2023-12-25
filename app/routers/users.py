from .. import models,utils,schemas
from http.client import HTTPException
from fastapi import HTTPException,Depends,APIRouter
from ..database import get_db,get_mongo_users,get_user_id
from sqlalchemy.orm import Session
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse

from .. import oAuth2
from bson import Binary
import io
#from typing import List

router = APIRouter(
    prefix='/user',
    tags = ['Users']
)

@router.post('/',status_code=201, response_model=schemas.UserResponse)
def create_user(user : schemas.UserCreate, db:Session = Depends(get_db)):
    user_fetched = db.query(models.User).filter(models.User.email == user.email).first()
    if user_fetched:
        raise HTTPException(status_code= 409,detail=f'User already exists')
    
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_data ={
         'id' : new_user.id
    }
    user_collection = get_mongo_users()
    id = user_collection.insert_one(user_data)
    print(id)
    return new_user

@router.post('/insert_pic',status_code=201)
def upload_profile_pic(file: UploadFile = File(...),user_id = Depends(oAuth2.get_current_user), db:Session = Depends(get_db)):
    if not file.content_type.startswith('image'):
        raise HTTPException(status_code=403,detail='Not an image file')
    user = get_user_id(user_id.id)
    users = get_mongo_users()
    file_data = file.file.read()
    binary_data = Binary(file_data)
    filter_criteria = {"_id": user['_id']}
    update_operation = {"$set": {"prof_pic": binary_data}}
    result = users.update_one(filter_criteria, update_operation)
    if result.matched_count == 0:
        raise HTTPException(status_code= 403, detail=f'Image not sent to server')
    return file.content_type

@router.get('/profile_pic/{id}')
def get_prof_pic(id:int, user_id = Depends(oAuth2.get_current_user)):
    user = get_user_id(user_id.id)
    users = get_mongo_users()
    if not user:
        raise HTTPException(status_code= 404, detail=f'User not found for {id}')
    query = {"id": id}  

    result = users.find_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    
    image = result.get("prof_pic")
    return StreamingResponse(io.BytesIO(image), media_type="image/jpeg")
    
@router.get('/{id}',response_model = schemas.UserResponse)
def getuser(id:int , db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= 404, detail=f'User not found for {id}')
    return user
