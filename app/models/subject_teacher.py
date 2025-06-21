from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class SubjectTeacher(Base):
    __tablename__ = "subject_teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    is_primary = Column(Boolean, default=False)  # Primary teacher for the subject
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    subject = relationship("Subject", back_populates="teachers")
    teacher = relationship("Teacher", back_populates="subjects")
    
    def __repr__(self):
        return f"<SubjectTeacher(subject_id={self.subject_id}, teacher_id={self.teacher_id})>" 