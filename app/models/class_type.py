from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class ClassType(Base):
    __tablename__ = "class_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    acronym = Column(String(10), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(7), nullable=True)  # Hex color code
    is_active = Column(Boolean, default=True)
    
    # Relationships
    schedules = relationship("Schedule", back_populates="class_type")
    
    def __repr__(self):
        return f"<ClassType(id={self.id}, name='{self.name}', acronym='{self.acronym}')>" 