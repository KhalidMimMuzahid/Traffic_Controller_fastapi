from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
# from base import Base
class Intersection(Base):
    __tablename__ = "intersections"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=False, index=True)
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=False)



