from fastapi import FastAPI
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


# try:
#     client = get_mongo()
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print('Exception caused')
#     print(e)    