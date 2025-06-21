from pydantic import BaseModel, Field
from typing import Optional


class ClassroomBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=20, description="Código único del aula")
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del aula")
    building: Optional[str] = Field(None, max_length=100, description="Edificio")
    floor: Optional[int] = Field(None, ge=0, le=50, description="Piso")
    capacity: Optional[int] = Field(None, ge=1, le=1000, description="Capacidad del aula")
    description: Optional[str] = Field(None, description="Descripción del aula")


class ClassroomCreate(ClassroomBase):
    pass


class ClassroomUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    building: Optional[str] = Field(None, max_length=100)
    floor: Optional[int] = Field(None, ge=0, le=50)
    capacity: Optional[int] = Field(None, ge=1, le=1000)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ClassroomResponse(ClassroomBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True 