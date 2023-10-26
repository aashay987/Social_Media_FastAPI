from logging import raiseExceptions
from fastapi import APIRouter,Response,Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,models,schemas,utils,oAuth2

router = APIRouter(
    tags= ['Authentication']
)

@router.post('/login',response_model= schemas.Token)
def login(user_cred:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(user_cred.username == models.User.email).first()
    if not user:
        raise HTTPException(status_code=403, detail=f'Invalid email or password')
    print(user.id)
    if(not(utils.verify(user_cred.password,user.password))):
        raise HTTPException(status_code=403, detail=f'Invalid email or password')

    Token = oAuth2.createacesstoken(data = {"id":user.id})

    return {"token" : Token,"token_type":"bearer"}
