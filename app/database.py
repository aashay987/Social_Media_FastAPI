from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting

#sql_alchemy_db_url = 'postgres://<username>:<password>@<ip address>/<hostname>/<database>'
SQL_ALCHEMY_DB_URL = f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'

engine = create_engine(SQL_ALCHEMY_DB_URL)
sessionLocal = sessionmaker(autoflush= False, bind= engine)
Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        

