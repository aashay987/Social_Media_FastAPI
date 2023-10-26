from .. import models,utils,schemas,oAuth2
from http.client import HTTPException
from fastapi import FastAPI,HTTPException,Depends,APIRouter
from ..database import engine,get_db,sessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

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
    return my_post

@router.delete('/{id}')
def delete_post(id:int, db:Session = Depends(get_db),current_user = Depends(oAuth2.get_current_user)):
    fetched_query = db.query(models.Post).filter(models.Post.id == id)
    fetched_post = fetched_query.first()
    if fetched_post.user_id != current_user.id:
        raise HTTPException(status_code=403 , detail= f'Not authorized to perform the action')
    
    if fetched_post:
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

####Code below has similar functionality but without sqlalchemy orm
### Need additional referencing to be done.
'''
@app.get("/post")
def get_post(db: Session = Depends(get_db)):
    cursor.execute("SELECT * from posts ")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get('/post/{id}')
def get_post(id:int):
    #The parameter is constraint as int, fast api sends id as string. Above line converts to string.
    #If not convertable will throw an error.
    cursor.execute("SELECT * FROM posts WHERE id = %s",[int(id)])
    fetched_post = cursor.fetchone()
    if not fetched_post:
        raise HTTPException(status_code= 404, detail= f"post with id = {id} not found")
    return {'post':fetched_post}

@app.post('/post',status_code=201)
def create_post(post:Post,response:Response):
    cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *", (post.title,post.content,post.published))
    my_post = cursor.fetchone()
    conn.commit()
    return {"message" : my_post}  

@app.delete('/post/{id}')
def delete_post(id:int,response:Response):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *",[int(id)])
    delete_post = cursor.fetchone()
    if not delete_post:
        raise HTTPException(status_code= 404, detail= f"post with id = {id} not found")
    conn.commit()
    return {"post" : delete_post}

@app.put('/post/{id}')
def update_post(id:int,post:Post,response:Response):
    cursor.execute("UPDATE posts SET title = %s,content= %s,published= %s WHERE id = %s RETURNING * ",(post.title,post.content,post.published,id))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(404,detail=f"Post with id = {id} not found")
    return {"updated post" : updated_post} 
    '''