from pydantic import BaseModel, Field
from typing import Optional, List


class SubjectBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=20, description="Código único de la asignatura")
    name: str = Field(..., min_length=1, max_length=200, description="Nombre de la asignatura")
    acronym: str = Field(..., min_length=1, max_length=10, description="Siglas de la asignatura")
    description: Optional[str] = Field(None, description="Descripción de la asignatura")
    credits: int = Field(..., ge=1, le=20, description="Número de créditos")


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    acronym: Optional[str] = Field(None, min_length=1, max_length=10)
    description: Optional[str] = None
    credits: Optional[int] = Field(None, ge=1, le=20)
    is_active: Optional[bool] = None


class SubjectResponse(SubjectBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True 