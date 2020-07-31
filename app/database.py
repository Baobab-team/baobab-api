import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, convert_unicode=True
)

Base = declarative_base()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)
