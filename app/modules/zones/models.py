from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
# from base import Base
class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=False, index=True)

     # Reverse relationship
     #Pattern:  field_name_that_mention_as_back_populates_values_in_another_model = relationship("Model_name_of_another", back_populates="field_name_of_another_model_that_refers_to_this_field", cascade="all, delete")
    cameras = relationship("Camera", back_populates="zone", cascade="all, delete")
    roads = relationship("Road", back_populates="zone", cascade="all, delete")
    intersections = relationship("Intersection", back_populates="zone", cascade="all, delete")
    vehicles = relationship("Vehicle", back_populates="zone", cascade="all, delete")



