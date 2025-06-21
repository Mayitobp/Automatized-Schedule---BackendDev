from sqlalchemy import Column, Integer, ForeignKey, String, Date, Time, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    class_type_id = Column(Integer, ForeignKey("class_types.id"), nullable=False)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    
    # Schedule details
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Semester information
    semester = Column(String(20), nullable=False)  # e.g., "2024-1", "2024-2"
    week_start = Column(Date, nullable=False)  # First week of the semester
    week_end = Column(Date, nullable=False)    # Last week of the semester
    
    # Additional information
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    subject = relationship("Subject", back_populates="schedules")
    class_type = relationship("ClassType", back_populates="schedules")
    classroom = relationship("Classroom", back_populates="schedules")
    teacher = relationship("Teacher")
    
    def __repr__(self):
        return f"<Schedule(id={self.id}, subject_id={self.subject_id}, day={self.day_of_week}, time={self.start_time}-{self.end_time})>" 