from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomUpdate, ClassroomResponse

router = APIRouter()


@router.post("/", response_model=ClassroomResponse, status_code=status.HTTP_201_CREATED)
def create_classroom(classroom: ClassroomCreate, db: Session = Depends(get_db)):
    """Crear un nuevo aula"""
    # Verificar si ya existe un aula con el mismo código
    db_classroom = db.query(Classroom).filter(Classroom.code == classroom.code).first()
    if db_classroom:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un aula con este código"
        )
    
    db_classroom = Classroom(**classroom.model_dump())
    db.add(db_classroom)
    db.commit()
    db.refresh(db_classroom)
    return db_classroom


@router.get("/", response_model=List[ClassroomResponse])
def get_classrooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de aulas"""
    classrooms = db.query(Classroom).offset(skip).limit(limit).all()
    return classrooms


@router.get("/{classroom_id}", response_model=ClassroomResponse)
def get_classroom(classroom_id: int, db: Session = Depends(get_db)):
    """Obtener un aula por ID"""
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula no encontrada"
        )
    return classroom


@router.put("/{classroom_id}", response_model=ClassroomResponse)
def update_classroom(classroom_id: int, classroom: ClassroomUpdate, db: Session = Depends(get_db)):
    """Actualizar un aula"""
    db_classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if db_classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula no encontrada"
        )
    
    # Verificar si el nuevo código ya existe (si se está actualizando)
    if classroom.code and classroom.code != db_classroom.code:
        existing_classroom = db.query(Classroom).filter(Classroom.code == classroom.code).first()
        if existing_classroom:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un aula con este código"
            )
    
    update_data = classroom.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_classroom, field, value)
    
    db.commit()
    db.refresh(db_classroom)
    return db_classroom


@router.delete("/{classroom_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_classroom(classroom_id: int, db: Session = Depends(get_db)):
    """Eliminar un aula (soft delete)"""
    db_classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if db_classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula no encontrada"
        )
    
    db_classroom.is_active = False
    db.commit()
    return None 