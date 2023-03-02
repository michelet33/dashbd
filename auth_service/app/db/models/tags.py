from sqlalchemy.orm import relationship, Mapped
from ..database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer
from sqlalchemy.sql import func
# from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from pydantic import BaseModel, constr
from datetime import datetime
from typing import List


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(75), unique=True)
    valid = Column(Boolean, default=True)
    user_created = Column(String(75), unique=False)
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    user_updated = Column(String(75), unique=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())
    # children: Mapped[List["Params"]] = relationship(back_populates="parent")

class TagsModel(BaseModel):
    id: str
    name: constr(max_length=75)
    valid: int
    user_created: str
    created_at: datetime
    user_updated: str
    updated_at: datetime

    class Config:
        orm_mode = True

class ListTags(BaseModel):
    status: str
    results: int
    tags: List[TagsModel]