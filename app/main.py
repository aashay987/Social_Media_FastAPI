#from typing import Optional,List
from fastapi import FastAPI
import psycopg2
#from psycopg2.extras import RealDictCursor
from .import models 
from .database import engine
#from sqlalchemy.orm import Session
from .routers import posts,users,auth,votes

from fastapi.middleware.cors import CORSMiddleware



#Since we are now using Alembic we dont need to run below commands to create the tables on startup.
#models.Base.metadata.create_all(bind=engine)


# while True:
#     try:    
#         conn = psycopg2.connect(host='localhost',database='fastAPI',user='postgres',password='aashay98',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful')
#         break
#     except Exception as error:
#         print(" Error failed to connect to dalabase!\n", error)
            
app =FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)

