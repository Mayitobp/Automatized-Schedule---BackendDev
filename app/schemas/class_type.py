from pydantic import BaseModel, Field
from typing import Optional


class ClassTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del tipo de clase")
    acronym: str = Field(..., min_length=1, max_length=10, description="Siglas del tipo de clase")
    description: Optional[str] = Field(None, description="Descripción del tipo de clase")
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$', description="Color en formato hexadecimal")


class ClassTypeCreate(ClassTypeBase):
    pass


class ClassTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    acronym: Optional[str] = Field(None, min_length=1, max_length=10)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    is_active: Optional[bool] = None


class ClassTypeResponse(ClassTypeBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True 