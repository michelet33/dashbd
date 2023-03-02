from ..database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer
from sqlalchemy.sql import func
# from fastapi_utils.guid_type import GUID
from pydantic import BaseModel, constr
from typing import List
import uuid


class Chargers(Base):
    __tablename__ = 'chargers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    charger_id = Column(String(100), index=True)
    charge_point_model= Column(String(255), index=True)
    charge_point_vendor= Column(String(255), index=True)
    connectors = Column(String(1500), index=True)
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, index=True, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, index=True, server_default=func.now())
    valid = Column(Boolean, default=True)

    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ChargersModel(BaseModel):
    charger_id: constr(max_length=100)
    charge_point_model: constr(max_length=255)
    charge_point_vendor: constr(max_length=255)
    connectors: constr(max_length=1500)

    class Config:
        orm_mode = True

class ListChargers(BaseModel):
    status: str
    results: int
    chargers: List[ChargersModel]
