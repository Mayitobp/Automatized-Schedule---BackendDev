from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse

router = APIRouter()


@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    """Crear un nuevo profesor"""
    # Verificar si ya existe un profesor con el mismo employee_id
    db_teacher = db.query(Teacher).filter(Teacher.employee_id == teacher.employee_id).first()
    if db_teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un profesor con este ID de empleado"
        )
    
    # Verificar si ya existe un profesor con el mismo email
    db_teacher = db.query(Teacher).filter(Teacher.email == teacher.email).first()
    if db_teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un profesor con este email"
        )
    
    db_teacher = Teacher(**teacher.model_dump())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


@router.get("/", response_model=List[TeacherResponse])
def get_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de profesores"""
    teachers = db.query(Teacher).offset(skip).limit(limit).all()
    return teachers


@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    """Obtener un profesor por ID"""
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )
    return teacher


@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(teacher_id: int, teacher: TeacherUpdate, db: Session = Depends(get_db)):
    """Actualizar un profesor"""
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )
    
    # Verificar si el nuevo employee_id ya existe (si se está actualizando)
    if teacher.employee_id and teacher.employee_id != db_teacher.employee_id:
        existing_teacher = db.query(Teacher).filter(Teacher.employee_id == teacher.employee_id).first()
        if existing_teacher:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un profesor con este ID de empleado"
            )
    
    # Verificar si el nuevo email ya existe (si se está actualizando)
    if teacher.email and teacher.email != db_teacher.email:
        existing_teacher = db.query(Teacher).filter(Teacher.email == teacher.email).first()
        if existing_teacher:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un profesor con este email"
            )
    
    update_data = teacher.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_teacher, field, value)
    
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    """Eliminar un profesor (soft delete)"""
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )
    
    db_teacher.is_active = False
    db.commit()
    return None 