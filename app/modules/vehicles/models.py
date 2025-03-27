from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean,  DateTime, LargeBinary
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from database import Base




class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String,  unique=False, index=False)
    direction = Column(String,  unique=False, index=False)
    len_violation= Column(Boolean,  unique=False, index=False)
    speed_violation= Column(Boolean,  unique=False, index=False)
    speed= Column(String,  unique=False, index=False)
    tracker_id= Column(Integer,  unique=False, index=False)
    photo = Column(String, nullable=True)  # Store binary image as BLOB
    license_photo= Column(String, nullable=True)  #
    license_number= Column(String,  nullable=True)


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
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
