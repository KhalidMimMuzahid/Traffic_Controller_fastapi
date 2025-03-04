from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
# from base import Base
class Intersection(Base):
    __tablename__ = "intersections"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=False, index=True)
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=False)

    # relationship 
    # Pattern:  field_name_that_mention_as_back_populates_values_in_another_model = relationship("Model_nama_of_targeted_table", back_populates="field_name_of_another_model_that_refers_to_this_field")
    zone = relationship("Zone", back_populates="intersections")

    # Reverse relationship
     #Pattern:  field_name_that_mention_as_back_populates_values_in_another_model = relationship("Model_name_of_another", back_populates="field_name_of_another_model_that_refers_to_this_field", cascade="all, delete")
    cameras = relationship("Camera", back_populates="intersection", cascade="all, delete")
    roads = relationship("Road", back_populates="intersection", cascade="all, delete")



