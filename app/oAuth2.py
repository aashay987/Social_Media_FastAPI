from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def createacesstoken(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_token

def verify_accesstoken(token:str,credential_exc):
    #print('Hello')
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str = payload.get("id")
        print(payload)
        print(id)
        if id is None:  
            raise credential_exc
        token_data = schemas.TokenData(id=id)
    
    except JWTError as e: 
        #print(e)
        raise credential_exc
    
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    cred_scp = HTTPException(status_code=401,detail = f'Could not validate credentials', headers={"www-Authenticate":"Bearer"})
    token = verify_accesstoken(token, cred_scp)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
