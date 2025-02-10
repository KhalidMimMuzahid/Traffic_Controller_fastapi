from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
# from base import Base
class Intersection(Base):
    __tablename__ = "intersections"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=False, index=True)
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=False)

    # Reverse relationship to Camera
    cameras = relationship("Camera", back_populates="intersection", cascade="all, delete")



