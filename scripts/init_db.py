#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos de ejemplo
"""
import sys
import os
from datetime import date, time

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import *
from app.database import Base

def init_db():
    """Inicializar la base de datos con datos de ejemplo"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Crear tipos de clase
        class_types = [
            ClassType(
                name="Conferencia",
                acronym="CONF",
                description="Clase magistral",
                color="#FF6B6B"
            ),
            ClassType(
                name="Laboratorio",
                acronym="LAB",
                description="Clase práctica en laboratorio",
                color="#4ECDC4"
            ),
            ClassType(
                name="Clase Práctica",
                acronym="CP",
                description="Clase práctica",
                color="#45B7D1"
            ),
            ClassType(
                name="Seminario",
                acronym="SEM",
                description="Seminario",
                color="#96CEB4"
            ),
            ClassType(
                name="Prueba Parcial",
                acronym="PP",
                description="Evaluación parcial",
                color="#FFEAA7"
            ),
            ClassType(
                name="Prueba Final",
                acronym="PF",
                description="Evaluación final",
                color="#DDA0DD"
            )
        ]
        
        for class_type in class_types:
            db.add(class_type)
        db.commit()
        print("✓ Tipos de clase creados")
        
        # Crear profesores
        teachers = [
            Teacher(
                employee_id="T001",
                first_name="Juan",
                last_name="Pérez",
                email="juan.perez@cujae.edu.cu",
                phone="+53 5 123 4567",
                department="Informática"
            ),
            Teacher(
                employee_id="T002",
                first_name="María",
                last_name="García",
                email="maria.garcia@cujae.edu.cu",
                phone="+53 5 234 5678",
                department="Matemáticas"
            ),
            Teacher(
                employee_id="T003",
                first_name="Carlos",
                last_name="López",
                email="carlos.lopez@cujae.edu.cu",
                phone="+53 5 345 6789",
                department="Física"
            ),
            Teacher(
                employee_id="T004",
                first_name="Ana",
                last_name="Martínez",
                email="ana.martinez@cujae.edu.cu",
                phone="+53 5 456 7890",
                department="Química"
            )
        ]
        
        for teacher in teachers:
            db.add(teacher)
        db.commit()
        print("✓ Profesores creados")
        
        # Crear asignaturas
        subjects = [
            Subject(
                code="INF101",
                name="Programación I",
                acronym="PROG1",
                description="Fundamentos de programación",
                credits=4
            ),
            Subject(
                code="INF102",
                name="Programación II",
                acronym="PROG2",
                description="Programación orientada a objetos",
                credits=4
            ),
            Subject(
                code="MAT101",
                name="Cálculo I",
                acronym="CALC1",
                description="Cálculo diferencial e integral",
                credits=5
            ),
            Subject(
                code="FIS101",
                name="Física I",
                acronym="FIS1",
                description="Mecánica clásica",
                credits=4
            ),
            Subject(
                code="QUI101",
                name="Química General",
                acronym="QUIM",
                description="Fundamentos de química",
                credits=3
            )
        ]
        
        for subject in subjects:
            db.add(subject)
        db.commit()
        print("✓ Asignaturas creadas")
        
        # Crear aulas
        classrooms = [
            Classroom(
                code="A101",
                name="Aula 101",
                building="Edificio A",
                floor=1,
                capacity=30
            ),
            Classroom(
                code="A102",
                name="Aula 102",
                building="Edificio A",
                floor=1,
                capacity=30
            ),
            Classroom(
                code="LAB1",
                name="Laboratorio 1",
                building="Edificio B",
                floor=1,
                capacity=20
            ),
            Classroom(
                code="LAB2",
                name="Laboratorio 2",
                building="Edificio B",
                floor=1,
                capacity=20
            ),
            Classroom(
                code="A201",
                name="Aula 201",
                building="Edificio A",
                floor=2,
                capacity=40
            )
        ]
        
        for classroom in classrooms:
            db.add(classroom)
        db.commit()
        print("✓ Aulas creadas")
        
        # Crear relaciones asignatura-profesor
        subject_teachers = [
            SubjectTeacher(subject_id=1, teacher_id=1, is_primary=True),
            SubjectTeacher(subject_id=2, teacher_id=1, is_primary=True),
            SubjectTeacher(subject_id=3, teacher_id=2, is_primary=True),
            SubjectTeacher(subject_id=4, teacher_id=3, is_primary=True),
            SubjectTeacher(subject_id=5, teacher_id=4, is_primary=True),
        ]
        
        for st in subject_teachers:
            db.add(st)
        db.commit()
        print("✓ Relaciones asignatura-profesor creadas")
        
        # Crear horarios de ejemplo
        schedules = [
            # Programación I - Lunes 8:00-10:00
            Schedule(
                subject_id=1,
                class_type_id=1,  # Conferencia
                classroom_id=1,
                teacher_id=1,
                day_of_week=0,  # Lunes
                start_time=time(8, 0),
                end_time=time(10, 0),
                semester="2024-1",
                week_start=date(2024, 2, 5),
                week_end=date(2024, 6, 28)
            ),
            # Programación I - Miércoles 14:00-16:00 (Laboratorio)
            Schedule(
                subject_id=1,
                class_type_id=2,  # Laboratorio
                classroom_id=3,
                teacher_id=1,
                day_of_week=2,  # Miércoles
                start_time=time(14, 0),
                end_time=time(16, 0),
                semester="2024-1",
                week_start=date(2024, 2, 5),
                week_end=date(2024, 6, 28)
            ),
            # Cálculo I - Martes 8:00-10:00
            Schedule(
                subject_id=3,
                class_type_id=1,  # Conferencia
                classroom_id=2,
                teacher_id=2,
                day_of_week=1,  # Martes
                start_time=time(8, 0),
                end_time=time(10, 0),
                semester="2024-1",
                week_start=date(2024, 2, 5),
                week_end=date(2024, 6, 28)
            ),
            # Física I - Jueves 10:00-12:00
            Schedule(
                subject_id=4,
                class_type_id=1,  # Conferencia
                classroom_id=5,
                teacher_id=3,
                day_of_week=3,  # Jueves
                start_time=time(10, 0),
                end_time=time(12, 0),
                semester="2024-1",
                week_start=date(2024, 2, 5),
                week_end=date(2024, 6, 28)
            ),
            # Química General - Viernes 14:00-16:00
            Schedule(
                subject_id=5,
                class_type_id=1,  # Conferencia
                classroom_id=1,
                teacher_id=4,
                day_of_week=4,  # Viernes
                start_time=time(14, 0),
                end_time=time(16, 0),
                semester="2024-1",
                week_start=date(2024, 2, 5),
                week_end=date(2024, 6, 28)
            )
        ]
        
        for schedule in schedules:
            db.add(schedule)
        db.commit()
        print("✓ Horarios de ejemplo creados")
        
        print("\n🎉 Base de datos inicializada exitosamente!")
        print("\nDatos creados:")
        print(f"- {len(class_types)} tipos de clase")
        print(f"- {len(teachers)} profesores")
        print(f"- {len(subjects)} asignaturas")
        print(f"- {len(classrooms)} aulas")
        print(f"- {len(schedules)} horarios de ejemplo")
        
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando base de datos...")
    init_db() 