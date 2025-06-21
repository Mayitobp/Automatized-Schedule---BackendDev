from sqlalchemy import Column, Integer, String, Text, Boolean, Integer
from sqlalchemy.orm import relationship
from app.database import Base


class Classroom(Base):
    __tablename__ = "classrooms"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    building = Column(String(100), nullable=True)
    floor = Column(Integer, nullable=True)
    capacity = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    schedules = relationship("Schedule", back_populates="classroom")
    
    def __repr__(self):
        return f"<Classroom(id={self.id}, code='{self.code}', name='{self.name}')>" 