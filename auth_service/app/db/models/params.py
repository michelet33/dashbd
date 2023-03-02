from sqlalchemy.orm import Mapped
from ..database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.sql import func
from pydantic import BaseModel, constr
from typing import List
from .tags import Tags


class Params(Base):
    __tablename__ = 'params'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # id_tags = Mapped[int] = Column(ForeignKey("tags.id"))
    id_tags = Column(Integer, index=True)
    name = Column(String(75), index=True)
    content = Column(String(1500))
    order = Column(Integer, index=True, default=0)
    created_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, index=True, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, index=True, server_default=func.now())
    valid = Column(Boolean, default=True)


# registry.map_imperatively(
#     Params,
#     Tags,
#     properties={"params_children": relationship("Tags", back_populates="tags_parent")},
# )

class ParamsModel(BaseModel):
    id_tags: int
    name: constr(max_length=75)
    content: constr(max_length=1500)

    class Config:
        orm_mode = True

class ListParams(BaseModel):
    status: str
    results: int
    logs: List[ParamsModel]
