from sqlalchemy import Column, Integer, String
from database import Base
class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=False, index=True)



