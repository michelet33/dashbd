import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from fastapi import Request
from fastapi_utils.guid_type import setup_guids_postgresql

DB_URL= ""
if settings.DATABASE_TYPE == 'POSTGRES':
    DB_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"
if settings.DATABASE_TYPE == 'SQLITE':
    path = os.getcwd()
    print(path)
    DB = os.path.join(path, "db/","base.db")
    DB_URL = f"sqlite:///{DB}"

engine = create_engine(
    DB_URL, echo=True, connect_args={"check_same_thread": False}
)
if settings.DATABASE_TYPE == 'POSTGRES':
    setup_guids_postgresql(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db(request: Request):
    # store arbitrary objects attached to the request itself, like the database session in this case
    return request.state.db

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()