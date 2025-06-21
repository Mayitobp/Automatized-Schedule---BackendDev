from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class TeacherBase(BaseModel):
    employee_id: str = Field(..., min_length=1, max_length=20, description="ID de empleado")
    first_name: str = Field(..., min_length=1, max_length=100, description="Nombre")
    last_name: str = Field(..., min_length=1, max_length=100, description="Apellido")
    email: EmailStr = Field(..., description="Email del profesor")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono")
    department: Optional[str] = Field(None, max_length=100, description="Departamento")


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    employee_id: Optional[str] = Field(None, min_length=1, max_length=20)
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class TeacherResponse(TeacherBase):
    id: int
    is_active: bool
    full_name: str
    
    class Config:
        from_attributes = True 