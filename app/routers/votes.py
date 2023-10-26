from .. import models,utils,schemas
from http.client import HTTPException
from fastapi import HTTPException,Depends,APIRouter
from ..database import engine,get_db,sessionLocal
from sqlalchemy.orm import Session
from .. import oAuth2 
router = APIRouter(
    prefix='/vote',
    tags = ['Votes']
)

@router.post('/',status_code=201)
def update_vote(vote:schemas.Vote,db: Session = Depends(get_db),user = Depends(oAuth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404,detail=f'Post with id {vote.post_id} not found.')
    
    fetched_res = db.query(models.Votes).filter(models.Votes.post_id ==vote.post_id,models.Votes.user_id == user.id)
    if fetched_res.first():
        if vote.vote_dir == 0:
            #Delete from table
            fetched_res.delete(synchronize_session=False)
            db.commit()
            return {"Vote successfuly removed"}
        
        raise HTTPException(status_code=409,detail=f"user {user.id} has alredy voted on post {vote.post_id}")
    
    else:
        if(vote.vote_dir == 1):
            new_vote = models.Votes(post_id = vote.post_id,user_id = user.id)
            db.add(new_vote)
            db.commit()
            return {"Vote successfuly added"}

        else:
            raise HTTPException(status_code= 404, detail=f'Vote does not exist.')