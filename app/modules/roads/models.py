from sqlalchemy import Column, Integer, String, Enum, ForeignKey
import enum
from sqlalchemy.orm import relationship
from database import Base




class Road(Base):
    __tablename__ = "roads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=False, index=False, nullable=False)
    road_no = Column(Integer, nullable=False)
    intersection_id = Column(Integer, ForeignKey('intersections.id'), nullable=False)
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=False)

    # relationship 
    # Pattern:  field_name_that_mention_as_back_populates_values_in_another_model = relationship("Model_nama_of_targeted_table", back_populates="field_name_of_another_model_that_refers_to_this_field")
    intersection = relationship("Intersection", back_populates="roads")
    zone = relationship("Zone", back_populates="roads")

    # Reverse relationship
     #Pattern:  field_name_that_mention_as_back_populates_values_in_another_model = relationship("Model_name_of_another", back_populates="field_name_of_another_model_that_refers_to_this_field", cascade="all, delete")
    cameras = relationship("Camera", back_populates="road", cascade="all, delete")



