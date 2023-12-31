from .. import models,utils,schemas,oAuth2
from http.client import HTTPException
from fastapi import UploadFile, File,HTTPException,Depends,APIRouter
from ..database import get_db,get_mongo_posts
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from bson import Binary
from fastapi.responses import StreamingResponse
import io
import zipfile

router = APIRouter(
    prefix='/post',
    tags= ['Posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db),user_id = Depends(oAuth2.get_current_user),limit:int = 10,skip:int = 0,search: Optional[str]= ''):
    #limit is query parameter 
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    fetched_posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).filter(models.Post.title.contains(search)).group_by(models.Post.id).limit(limit).offset(skip).all()

    return fetched_posts

@router.get('/{id}',response_model=schemas.PostOut)
def get_post(id:int,db:Session = Depends(get_db),user_id = Depends(oAuth2.get_current_user)):
    #fetched_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    # fetched_post1 = db.query(models.Post,func.count(models.Votes.post_id)).join(
    #     models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    
    fetched_post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    
    if fetched_post:

        return fetched_post
    raise HTTPException(status_code= 404, detail= 'Element not found') 

@router.post('/',status_code=201, response_model=schemas.PostResponse)
def create_post(post :schemas.PostCreate,db:Session = Depends(get_db),current_user = Depends(oAuth2.get_current_user)):
    my_post = models.Post(**post.dict(),user_id = current_user.id)
    db.add(my_post)
    db.commit()
    db.refresh(my_post) # just for returing the newly added entry while running query
    posts = get_mongo_posts()
    post ={
         'id' : my_post.id,
         'images' : []
    }
    posts.insert_one(post)
    return my_post

@router.delete('/{id}')
def delete_post(id:int, db:Session = Depends(get_db),current_user = Depends(oAuth2.get_current_user)):
    fetched_query = db.query(models.Post).filter(models.Post.id == id)
    fetched_post = fetched_query.first()
    if fetched_post.user_id != current_user.id:
        raise HTTPException(status_code=403 , detail= f'Not authorized to perform the action')
    
    if fetched_post:
        posts = get_mongo_posts()
        posts.delete_one({'id':id})
        fetched_query.delete(synchronize_session=False)
        db.commit()
        return {"Deleted Message" : id}
    raise HTTPException(status_code= 404, detail= 'Element not found') 


@router.put('/{id}',response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.PostCreate,db:Session = Depends(get_db),current_user = Depends(oAuth2.get_current_user)):
    fetched_query = db.query(models.Post).filter(models.Post.id == id)
    fetched_post = fetched_query.first()
    if fetched_post == None:
        raise HTTPException (status_code=404, detail='Element not found')
    
    if fetched_post.user_id != current_user.id:
        raise HTTPException(status_code=403 , detail= f'Not authorized to perform the action')
    
    fetched_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return fetched_post

@router.post('/image/{id}')
def add_image_post(id:int, files: List[UploadFile] = File(...),db:Session = Depends(get_db),current_user = Depends(oAuth2.get_current_user)):
    fetched_query = db.query(models.Post).filter(models.Post.id == id)
    fetched_post = fetched_query.first()
    if fetched_post == None:
        raise HTTPException (status_code=404, detail='Post not found')
        
    if fetched_post.user_id != current_user.id:
        raise HTTPException(status_code= 403, detail= f'Not authorized to perform this action')
    posts = get_mongo_posts()
    
    document_query = {"id": id}  # Replace with the actual document identifier
    encoded_files = []
    for file in files:
        encoded_files.append(Binary(file.file.read()))
    update_query = {"$push": {"images": {"$each": encoded_files}}}
    posts.update_one(document_query, update_query)
    return len(files)

@router.get('/image/{id}')
def get_images(id:int,db:Session = Depends(get_db),current_user = Depends(oAuth2.get_current_user)):
    fetched_query = db.query(models.Post).filter(models.Post.id == id)
    fetched_post = fetched_query.first()
    if fetched_post == None:
        raise HTTPException (status_code=404, detail='Post not found')
        
    if fetched_post.user_id != current_user.id:
        raise HTTPException(status_code= 403, detail= f'Not authorized to perform this action')
    posts = get_mongo_posts()
    query = {"id": id}
    result = posts.find_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        images_from_db = result.get("images")


        for i,image_bytes in enumerate(images_from_db):
            
            if image_bytes:
                image_filename = f"{i}.png"
                zip_file.writestr(image_filename, image_bytes)

    zip_content = zip_buffer.getvalue()

    return StreamingResponse(io.BytesIO(zip_content), media_type="application/zip", headers={'Content-Disposition': 'attachment; filename="images.zip"'})

