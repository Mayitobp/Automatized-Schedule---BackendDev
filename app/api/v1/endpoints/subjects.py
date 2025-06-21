from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectUpdate, SubjectResponse

router = APIRouter()


@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    """Crear una nueva asignatura"""
    # Verificar si ya existe una asignatura con el mismo código
    db_subject = db.query(Subject).filter(Subject.code == subject.code).first()
    if db_subject:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una asignatura con este código"
        )
    
    db_subject = Subject(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


@router.get("/", response_model=List[SubjectResponse])
def get_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de asignaturas"""
    subjects = db.query(Subject).offset(skip).limit(limit).all()
    return subjects


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    """Obtener una asignatura por ID"""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignatura no encontrada"
        )
    return subject


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(subject_id: int, subject: SubjectUpdate, db: Session = Depends(get_db)):
    """Actualizar una asignatura"""
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignatura no encontrada"
        )
    
    # Verificar si el nuevo código ya existe (si se está actualizando)
    if subject.code and subject.code != db_subject.code:
        existing_subject = db.query(Subject).filter(Subject.code == subject.code).first()
        if existing_subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una asignatura con este código"
            )
    
    update_data = subject.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_subject, field, value)
    
    db.commit()
    db.refresh(db_subject)
    return db_subject


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    """Eliminar una asignatura (soft delete)"""
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignatura no encontrada"
        )
    
    db_subject.is_active = False
    db.commit()
    return None 