from pydantic import BaseModel, Field
from typing import Optional


class SubjectTeacherBase(BaseModel):
    subject_id: int = Field(..., description="ID de la asignatura")
    teacher_id: int = Field(..., description="ID del profesor")
    is_primary: bool = Field(False, description="Indica si es el profesor principal")


class SubjectTeacherCreate(SubjectTeacherBase):
    pass


class SubjectTeacherResponse(SubjectTeacherBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True 