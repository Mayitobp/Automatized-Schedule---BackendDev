from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time


class ScheduleBase(BaseModel):
    subject_id: int = Field(..., description="ID de la asignatura")
    class_type_id: int = Field(..., description="ID del tipo de clase")
    classroom_id: int = Field(..., description="ID del aula")
    teacher_id: int = Field(..., description="ID del profesor")
    day_of_week: int = Field(..., ge=0, le=6, description="Día de la semana (0=Lunes, 6=Domingo)")
    start_time: time = Field(..., description="Hora de inicio")
    end_time: time = Field(..., description="Hora de fin")
    semester: str = Field(..., min_length=1, max_length=20, description="Semestre (ej: 2024-1)")
    week_start: date = Field(..., description="Fecha de inicio del semestre")
    week_end: date = Field(..., description="Fecha de fin del semestre")
    notes: Optional[str] = Field(None, description="Notas adicionales")


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    subject_id: Optional[int] = None
    class_type_id: Optional[int] = None
    classroom_id: Optional[int] = None
    teacher_id: Optional[int] = None
    day_of_week: Optional[int] = Field(None, ge=0, le=6)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    semester: Optional[str] = Field(None, min_length=1, max_length=20)
    week_start: Optional[date] = None
    week_end: Optional[date] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class ScheduleResponse(ScheduleBase):
    id: int
    is_active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True 