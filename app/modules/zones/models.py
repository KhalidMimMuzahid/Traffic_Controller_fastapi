from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
# from base import Base
class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=False, index=True)
     # Reverse relationship to Camera
    cameras = relationship("Camera", back_populates="zone", cascade="all, delete")



