from sqlalchemy import Column, Integer, String, Enum, ForeignKey
import enum
from sqlalchemy.orm import relationship
from database import Base

# Define an enumeration for directionType
class DirectionTypeEnum(enum.Enum):
    entry = "entry"
    exit = "exit"


class Camera(Base):
    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=False, index=False)
    road_no = Column(Integer, nullable=False)
    road_name = Column(String, nullable=False)
    direction_type = Column(Enum(DirectionTypeEnum), nullable=False)
    intersection_id = Column(Integer, ForeignKey('intersections.id'), nullable=False)
    intersection = relationship("Intersection", back_populates="cameras")
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=False)
    zone = relationship("Zone", back_populates="cameras")



