from ..database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID
from pydantic import BaseModel, constr
from typing import List
import uuid


class Logs(Base):
    __tablename__ = 'logs'
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    charger_id = Column(String(255), index=True)
    action = Column(String(75), index=True)
    content = Column(String(1500))
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, index=True, server_default=func.now())
    valid = Column(Boolean, default=True)

class LogsModel(BaseModel):
    charger_id: constr(max_length=255)
    action: constr(max_length=75)
    content: constr(max_length=1500)

    class Config:
        orm_mode = True

class ListLogs(BaseModel):
    status: str
    results: int
    notes: List[LogsModel]
