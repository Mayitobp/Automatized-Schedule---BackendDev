from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    acronym = Column(String(10), nullable=False)
    description = Column(Text, nullable=True)
    credits = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    teachers = relationship("SubjectTeacher", back_populates="subject")
    schedules = relationship("Schedule", back_populates="subject")
    
    def __repr__(self):
        return f"<Subject(id={self.id}, code='{self.code}', name='{self.name}')>" 