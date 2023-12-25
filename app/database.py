from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting
#from .main import app


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#sql_alchemy_db_url = 'postgres://<username>:<password>@<ip address>/<hostname>/<database>'
SQL_ALCHEMY_DB_URL = f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'
MONGODB_URL = f'mongodb+srv://{setting.mongodb_username}:{setting.mongodb_password}@{setting.mongodb_cluster}.mongodb.net/?retryWrites=true&w=majority'


engine = create_engine(SQL_ALCHEMY_DB_URL)
sessionLocal = sessionmaker(autoflush= False, bind= engine)
Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_mongo_users():
    client = MongoClient(MONGODB_URL, server_api=ServerApi('1'))
    db = client[setting.mongodb_db]
    collection = db[setting.mongodb_collection_users]
    return collection
    
def get_mongo_posts():
    client = MongoClient(MONGODB_URL, server_api=ServerApi('1'))
    db = client[setting.mongodb_db]
    collection = db[setting.mongodb_collection_posts]
    return collection

def get_user_id(id):
    users = get_mongo_users()
    query = {"id":id}
    user = users.find_one(query)
    return user
