from ..base_class import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean
from sqlalchemy.sql import func

class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer,primary_key=True, autoincrement=True)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    user_price = Column(String(500))
    charging_price = Column(String(500))
    idle_price = Column(String(500))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, index=True, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, index=True, server_default=func.now())
    valid = Column(Boolean, default=True)

    # jobs = relationship("Job",back_populates="owner")