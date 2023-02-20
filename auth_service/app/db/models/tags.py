from ..database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from pydantic import BaseModel, constr
from datetime import datetime
from typing import List


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(GUID, primary_key=True,
                server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    name = Column(String(75), unique=True)
    valid = Column(Boolean, default=True)
    userCreate = Column(String(75), unique=False)
    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    userUpdate = Column(String(75), unique=False)
    updatedAt = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())

class TagsModel(BaseModel):
    id: str
    name: constr(max_length=75)
    valid: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True

class ListTags(BaseModel):
    status: str
    results: int
    notes: List[TagsModel]