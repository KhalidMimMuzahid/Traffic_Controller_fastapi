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
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=False)

    # relationship 
    # Pattern:  field_name_that_mention_as_back_populates_values_in_another_model = relationship("Model_nama_of_targeted_table", back_populates="field_name_of_another_model_that_refers_to_this_field")
    intersection = relationship("Intersection", back_populates="cameras")
    zone = relationship("Zone", back_populates="cameras")




