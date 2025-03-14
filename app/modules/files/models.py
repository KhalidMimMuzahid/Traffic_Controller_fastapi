import uuid
from sqlalchemy import Column, Integer, DateTime, LargeBinary, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID  # Use PostgreSQL UUID type

from database import Base


class File(Base):
    __tablename__ = "files"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True) 
    file_type= Column(String,  nullable=False )
    file = Column(LargeBinary, nullable=True)  # Store binary image as BLOB
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())