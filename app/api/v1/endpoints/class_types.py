from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.class_type import ClassType
from app.schemas.class_type import ClassTypeCreate, ClassTypeUpdate, ClassTypeResponse

router = APIRouter()


@router.post("/", response_model=ClassTypeResponse, status_code=status.HTTP_201_CREATED)
def create_class_type(class_type: ClassTypeCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tipo de clase"""
    # Verificar si ya existe un tipo de clase con el mismo nombre
    db_class_type = db.query(ClassType).filter(ClassType.name == class_type.name).first()
    if db_class_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un tipo de clase con este nombre"
        )
    
    # Verificar si ya existe un tipo de clase con las mismas siglas
    db_class_type = db.query(ClassType).filter(ClassType.acronym == class_type.acronym).first()
    if db_class_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un tipo de clase con estas siglas"
        )
    
    db_class_type = ClassType(**class_type.model_dump())
    db.add(db_class_type)
    db.commit()
    db.refresh(db_class_type)
    return db_class_type


@router.get("/", response_model=List[ClassTypeResponse])
def get_class_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de tipos de clase"""
    class_types = db.query(ClassType).offset(skip).limit(limit).all()
    return class_types


@router.get("/{class_type_id}", response_model=ClassTypeResponse)
def get_class_type(class_type_id: int, db: Session = Depends(get_db)):
    """Obtener un tipo de clase por ID"""
    class_type = db.query(ClassType).filter(ClassType.id == class_type_id).first()
    if class_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de clase no encontrado"
        )
    return class_type


@router.put("/{class_type_id}", response_model=ClassTypeResponse)
def update_class_type(class_type_id: int, class_type: ClassTypeUpdate, db: Session = Depends(get_db)):
    """Actualizar un tipo de clase"""
    db_class_type = db.query(ClassType).filter(ClassType.id == class_type_id).first()
    if db_class_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de clase no encontrado"
        )
    
    # Verificar si el nuevo nombre ya existe (si se está actualizando)
    if class_type.name and class_type.name != db_class_type.name:
        existing_class_type = db.query(ClassType).filter(ClassType.name == class_type.name).first()
        if existing_class_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un tipo de clase con este nombre"
            )
    
    # Verificar si las nuevas siglas ya existen (si se están actualizando)
    if class_type.acronym and class_type.acronym != db_class_type.acronym:
        existing_class_type = db.query(ClassType).filter(ClassType.acronym == class_type.acronym).first()
        if existing_class_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un tipo de clase con estas siglas"
            )
    
    update_data = class_type.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_class_type, field, value)
    
    db.commit()
    db.refresh(db_class_type)
    return db_class_type


@router.delete("/{class_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class_type(class_type_id: int, db: Session = Depends(get_db)):
    """Eliminar un tipo de clase (soft delete)"""
    db_class_type = db.query(ClassType).filter(ClassType.id == class_type_id).first()
    if db_class_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de clase no encontrado"
        )
    
    db_class_type.is_active = False
    db.commit()
    return None 