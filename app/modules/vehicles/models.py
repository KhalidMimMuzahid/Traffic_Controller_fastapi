from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean
import enum
from sqlalchemy.orm import relationship
from database import Base

# Define an enumeration for directionType
class DirectionTypeEnum(enum.Enum):
    entry = "entry"
    exit = "exit"


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String,  unique=False, index=False)
    direction_type = Column(Enum(DirectionTypeEnum), nullable=False)
    len_violation= Column(Boolean,  unique=False, index=False)
    speed_violation= Column(Boolean,  unique=False, index=False)
    speed= Column(Integer,  unique=False, index=False)
    tracker_id= Column(Integer,  unique=False, index=False)
    # photo 
    # license_photo
    license_number= Column(Integer,  unique=False, index=False)


    camera_id= Column(Integer, ForeignKey('cameras.id'), nullable=False)
    road_id= Column(Integer, ForeignKey('roads.id'), nullable=False)
    intersection_id = Column(Integer, ForeignKey('intersections.id'), nullable=False)
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=False)


    # relationship 
    # Pattern:  field_name_that_mention_as_back_populates_values_in_another_model = relationship("Model_nama_of_targeted_table", back_populates="field_name_of_another_model_that_refers_to_this_field")
    camera = relationship("Camera", back_populates="vehicles")
    road = relationship("Road", back_populates="vehicles")
    intersection = relationship("Intersection", back_populates="vehicles")
    zone = relationship("Zone", back_populates="vehicles")
    # timestamp 




