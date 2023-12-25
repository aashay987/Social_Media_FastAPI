from pydantic import BaseSettings

class  Setting(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str
    database_name : str
    database_username: str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int
    admin_password : str
    mongodb_username : str
    mongodb_password : str
    mongodb_cluster : str
    mongodb_db : str
    mongodb_collection_users : str
    mongodb_collection_posts : str
    class Config:
        env_file = '.env'

setting = Setting()
