# 🚀 Guía Completa de Backend Development: Sistema de Gestión de Horarios CUJAE

## 📋 Tabla de Contenidos

1. [Introducción y Arquitectura General](#introducción-y-arquitectura-general)
2. [Tecnologías y Stack Tecnológico](#tecnologías-y-stack-tecnológico)
3. [Arquitectura de Capas](#arquitectura-de-capas)
4. [Configuración y Gestión de Entorno](#configuración-y-gestión-de-entorno)
5. [Base de Datos y ORM](#base-de-datos-y-orm)
6. [Modelos de Datos](#modelos-de-datos)
7. [Esquemas y Validación](#esquemas-y-validación)
8. [API REST y Endpoints](#api-rest-y-endpoints)
9. [Validaciones de Negocio](#validaciones-de-negocio)
10. [Migraciones de Base de Datos](#migraciones-de-base-de-datos)
11. [Docker y Contenedores](#docker-y-contenedores)
12. [Testing y Calidad de Código](#testing-y-calidad-de-código)
13. [Despliegue y Producción](#despliegue-y-producción)
14. [Buenas Prácticas y Patrones](#buenas-prácticas-y-patrones)
15. [Escalabilidad y Performance](#escalabilidad-y-performance)

---

## 🎯 Introducción y Arquitectura General

### ¿Qué es este proyecto?

Este es un **microservicio de gestión de horarios académicos** desarrollado para la CUJAE (Universidad Tecnológica de La Habana). Es un ejemplo perfecto de una aplicación backend moderna que implementa las mejores prácticas de desarrollo.

### Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE (Frontend/Mobile)                │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/HTTPS
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   ROUTERS   │  │  MIDDLEWARE │  │ VALIDATION  │         │
│  │  (Endpoints)│  │   (CORS,    │  │ (Pydantic)  │         │
│  │             │  │   Auth)     │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────┬───────────────────────────────────────┘
                      │ SQLAlchemy ORM
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    POSTGRESQL DATABASE                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   TABLES    │  │  RELATIONS  │  │  INDEXES    │         │
│  │             │  │             │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### Principios de Diseño Aplicados

1. **Separación de Responsabilidades**: Cada capa tiene una responsabilidad específica
2. **Inversión de Dependencias**: Las capas superiores no dependen de las inferiores
3. **Single Responsibility Principle**: Cada módulo tiene una sola razón para cambiar
4. **Open/Closed Principle**: Abierto para extensión, cerrado para modificación

---

## 🛠️ Tecnologías y Stack Tecnológico

### Stack Principal

| Tecnología | Versión | Propósito | ¿Por qué se eligió? |
|------------|---------|-----------|---------------------|
| **Python** | 3.11+ | Lenguaje base | Sintaxis clara, ecosistema rico, tipado opcional |
| **FastAPI** | 0.104.1 | Framework web | Performance, auto-documentación, validación automática |
| **SQLAlchemy** | 2.0.23 | ORM | Potente, flexible, soporte para múltiples DBs |
| **PostgreSQL** | 15+ | Base de datos | ACID, JSON, escalabilidad, open source |
| **Pydantic** | 2.5.0 | Validación | Integración perfecta con FastAPI, tipado fuerte |
| **Alembic** | 1.12.1 | Migraciones | Herramienta oficial de SQLAlchemy |

### Dependencias Secundarias

```python
# requirements.txt - Análisis de cada dependencia
fastapi==0.104.1          # Framework web moderno y rápido
uvicorn[standard]==0.24.0 # Servidor ASGI para FastAPI
sqlalchemy==2.0.23        # ORM para Python
psycopg2-binary==2.9.9    # Driver PostgreSQL para Python
alembic==1.12.1           # Sistema de migraciones
pydantic==2.5.0           # Validación de datos y serialización
pydantic-settings==2.1.0  # Gestión de configuración
python-multipart==0.0.6   # Manejo de formularios multipart
openpyxl==3.1.2           # Generación de archivos Excel
python-dotenv==1.0.0      # Carga de variables de entorno
```

### ¿Por qué este Stack?

1. **FastAPI**: 
   - Performance comparable a Node.js y Go
   - Documentación automática con Swagger/OpenAPI
   - Validación automática con Pydantic
   - Soporte nativo para async/await

2. **SQLAlchemy**:
   - ORM más maduro de Python
   - Soporte para múltiples bases de datos
   - Sistema de migraciones robusto
   - Query builder potente

3. **PostgreSQL**:
   - Base de datos relacional más avanzada
   - Soporte para JSON, arrays, tipos personalizados
   - Excelente para aplicaciones complejas
   - Escalabilidad horizontal y vertical

---

## 🏗️ Arquitectura de Capas

### Estructura del Proyecto

```
cujae-calendar-ms/
├── app/                          # Código principal de la aplicación
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada de FastAPI
│   ├── config.py                 # Configuración de la aplicación
│   ├── database.py               # Configuración de la base de datos
│   ├── api/                      # Capa de API
│   │   └── v1/                   # Versionado de API
│   │       ├── api.py            # Router principal
│   │       └── endpoints/        # Endpoints específicos
│   │           ├── subjects.py
│   │           ├── teachers.py
│   │           ├── schedules.py
│   │           └── ...
│   ├── models/                   # Modelos de SQLAlchemy (Capa de Datos)
│   │   ├── subject.py
│   │   ├── teacher.py
│   │   ├── schedule.py
│   │   └── ...
│   └── schemas/                  # Esquemas Pydantic (Capa de Presentación)
│       ├── subject.py
│       ├── teacher.py
│       ├── schedule.py
│       └── ...
├── alembic/                      # Migraciones de base de datos
├── scripts/                      # Scripts de utilidad
├── requirements.txt              # Dependencias de Python
├── docker-compose.yml            # Orquestación de contenedores
├── Dockerfile                    # Imagen de Docker
└── README.md                     # Documentación
```

### Capas de la Arquitectura

#### 1. **Capa de Presentación (API Layer)**
```python
# app/api/v1/endpoints/schedules.py
@router.post("/", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    """Crear un nuevo horario"""
    # Lógica de negocio aquí
```

**Responsabilidades:**
- Manejo de requests HTTP
- Validación de entrada
- Serialización de respuesta
- Manejo de errores HTTP

#### 2. **Capa de Negocio (Business Layer)**
```python
# Lógica de validación de conflictos de horario
def check_schedule_conflicts(db: Session, schedule: ScheduleCreate):
    # Verificar conflictos de aula
    # Verificar conflictos de profesor
    # Retornar errores si existen conflictos
```

**Responsabilidades:**
- Reglas de negocio
- Validaciones complejas
- Lógica de aplicación
- Orquestación de operaciones

#### 3. **Capa de Datos (Data Layer)**
```python
# app/models/schedule.py
class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    # ... más campos
```

**Responsabilidades:**
- Definición de modelos de datos
- Relaciones entre entidades
- Operaciones CRUD básicas
- Mapeo objeto-relacional

---

## ⚙️ Configuración y Gestión de Entorno

### Sistema de Configuración

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://username:password@localhost:5432/cujae_calendar_db"
    
    # Application
    app_name: str = "CUJAE Calendar Management System"
    debug: bool = True
    secret_key: str = "your-secret-key-here"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### Variables de Entorno

```bash
# .env
DATABASE_URL=postgresql://username:password@localhost:5432/cujae_calendar_db
DEBUG=True
SECRET_KEY=your-secure-secret-key
HOST=0.0.0.0
PORT=8000
```

### Beneficios de esta Configuración

1. **Separación de Configuración**: Diferentes configuraciones para desarrollo, testing y producción
2. **Seguridad**: Credenciales sensibles fuera del código
3. **Flexibilidad**: Fácil cambio de configuración sin modificar código
4. **Validación**: Pydantic valida automáticamente los tipos de datos

---

## 🗄️ Base de Datos y ORM

### Configuración de SQLAlchemy

```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Crear engine de base de datos
engine = create_engine(settings.database_url)

# Crear SessionLocal para manejo de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para todos los modelos
Base = declarative_base()

# Dependency para inyección de dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Conceptos Clave de SQLAlchemy

#### 1. **Engine**
- Representa la conexión a la base de datos
- Maneja el pool de conexiones
- Configura el dialecto específico de la DB

#### 2. **Session**
- Contexto de trabajo con la base de datos
- Maneja transacciones
- Cache de objetos
- Lazy loading de relaciones

#### 3. **Base**
- Clase base para todos los modelos
- Proporciona funcionalidad común
- Permite crear tablas automáticamente

### Patrón de Inyección de Dependencias

```python
@router.get("/")
def get_items(db: Session = Depends(get_db)):
    # db es inyectado automáticamente por FastAPI
    items = db.query(Item).all()
    return items
```

**Beneficios:**
- Testing más fácil (mock de la base de datos)
- Separación de responsabilidades
- Reutilización de código
- Control de ciclo de vida de recursos

---

## 📊 Modelos de Datos

### Diseño de Modelos

```python
# app/models/schedule.py
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Time, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Schedule(Base):
    __tablename__ = "schedules"
    
    # Campos de identificación
    id = Column(Integer, primary_key=True, index=True)
    
    # Claves foráneas
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    class_type_id = Column(Integer, ForeignKey("class_types.id"), nullable=False)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    
    # Campos de horario
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 1=Tuesday, etc.
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Información del semestre
    semester = Column(String(20), nullable=False)  # "2024-1", "2024-2"
    week_start = Column(Date, nullable=False)
    week_end = Column(Date, nullable=False)
    
    # Campos de auditoría
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    subject = relationship("Subject", back_populates="schedules")
    class_type = relationship("ClassType", back_populates="schedules")
    classroom = relationship("Classroom", back_populates="schedules")
    teacher = relationship("Teacher")
```

### Tipos de Datos SQLAlchemy

| Tipo SQLAlchemy | Tipo PostgreSQL | Descripción |
|-----------------|-----------------|-------------|
| `Integer` | `INTEGER` | Números enteros |
| `String(20)` | `VARCHAR(20)` | Texto con longitud máxima |
| `Text` | `TEXT` | Texto sin límite de longitud |
| `Boolean` | `BOOLEAN` | Valores true/false |
| `DateTime` | `TIMESTAMP` | Fecha y hora |
| `Date` | `DATE` | Solo fecha |
| `Time` | `TIME` | Solo hora |
| `ForeignKey` | `FOREIGN KEY` | Clave foránea |

### Relaciones entre Modelos

#### 1. **One-to-Many**
```python
# Un Subject puede tener muchos Schedules
class Subject(Base):
    schedules = relationship("Schedule", back_populates="subject")

class Schedule(Base):
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    subject = relationship("Subject", back_populates="schedules")
```

#### 2. **Many-to-Many**
```python
# Un Subject puede tener muchos Teachers y viceversa
class SubjectTeacher(Base):
    __tablename__ = "subject_teachers"
    subject_id = Column(Integer, ForeignKey("subjects.id"), primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), primary_key=True)
    
    subject = relationship("Subject", back_populates="teachers")
    teacher = relationship("Teacher", back_populates="subjects")
```

### Índices y Optimización

```python
# Índices para mejorar performance
id = Column(Integer, primary_key=True, index=True)  # Índice automático
code = Column(String(20), unique=True, index=True)  # Índice único
```

**Tipos de Índices:**
- **Primary Key**: Automático, único, no nulo
- **Unique**: Garantiza valores únicos
- **Index**: Mejora velocidad de consultas
- **Composite Index**: Múltiples columnas

---

## 🔍 Esquemas y Validación

### Esquemas Pydantic

```python
# app/schemas/schedule.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

class ScheduleBase(BaseModel):
    subject_id: int = Field(..., description="ID de la asignatura")
    class_type_id: int = Field(..., description="ID del tipo de clase")
    classroom_id: int = Field(..., description="ID del aula")
    teacher_id: int = Field(..., description="ID del profesor")
    day_of_week: int = Field(..., ge=0, le=6, description="Día de la semana")
    start_time: time = Field(..., description="Hora de inicio")
    end_time: time = Field(..., description="Hora de fin")
    semester: str = Field(..., min_length=1, max_length=20)
    week_start: date = Field(..., description="Fecha de inicio del semestre")
    week_end: date = Field(..., description="Fecha de fin del semestre")
    notes: Optional[str] = Field(None, description="Notas adicionales")

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    subject_id: Optional[int] = None
    class_type_id: Optional[int] = None
    # ... otros campos opcionales

class ScheduleResponse(ScheduleBase):
    id: int
    is_active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True  # Permite crear desde objetos SQLAlchemy
```

### Patrón de Esquemas

#### 1. **Base Schema**
- Contiene campos comunes
- Define validaciones básicas
- Reutilizable para múltiples operaciones

#### 2. **Create Schema**
- Hereda de Base
- Usado para crear nuevos registros
- Todos los campos requeridos

#### 3. **Update Schema**
- Campos opcionales
- Permite actualizaciones parciales
- Validaciones específicas para updates

#### 4. **Response Schema**
- Hereda de Base
- Incluye campos generados (ID, timestamps)
- Configurado para serialización

### Validaciones Avanzadas

```python
from pydantic import validator

class ScheduleBase(BaseModel):
    # ... campos ...
    
    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v
    
    @validator('week_end')
    def week_end_must_be_after_week_start(cls, v, values):
        if 'week_start' in values and v <= values['week_start']:
            raise ValueError('week_end must be after week_start')
        return v
```

### Beneficios de Pydantic

1. **Validación Automática**: Valida tipos y restricciones automáticamente
2. **Serialización**: Convierte automáticamente entre JSON y objetos Python
3. **Documentación**: Genera automáticamente documentación OpenAPI
4. **Type Safety**: Proporciona hints de tipo para IDEs
5. **Performance**: Validación rápida con Rust (en versiones recientes)

---

## 🌐 API REST y Endpoints

### Estructura de Endpoints

```python
# app/api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import subjects, teachers, class_types, classrooms, schedules

api_router = APIRouter()

api_router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
api_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
api_router.include_router(class_types.router, prefix="/class-types", tags=["class-types"])
api_router.include_router(classrooms.router, prefix="/classrooms", tags=["classrooms"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["schedules"])
```

### Patrón CRUD Completo

```python
# app/api/v1/endpoints/schedules.py
@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    """Crear un nuevo horario"""
    # Validaciones de negocio
    # Crear registro
    # Retornar respuesta

@router.get("/", response_model=List[ScheduleResponse])
def get_schedules(
    skip: int = 0, 
    limit: int = 100, 
    semester: Optional[str] = None,
    teacher_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de horarios con filtros opcionales"""
    # Construir query con filtros
    # Paginar resultados
    # Retornar lista

@router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Obtener un horario por ID"""
    # Buscar por ID
    # Manejar 404
    # Retornar registro

@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(schedule_id: int, schedule: ScheduleUpdate, db: Session = Depends(get_db)):
    """Actualizar un horario"""
    # Buscar registro
    # Validar cambios
    # Actualizar
    # Retornar actualizado

@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Eliminar un horario (soft delete)"""
    # Buscar registro
    # Soft delete
    # Retornar 204
```

### HTTP Status Codes

| Código | Significado | Uso |
|--------|-------------|-----|
| 200 | OK | GET exitoso |
| 201 | Created | POST exitoso |
| 204 | No Content | DELETE exitoso |
| 400 | Bad Request | Datos inválidos |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Validación fallida |
| 500 | Internal Server Error | Error del servidor |

### Query Parameters y Filtros

```python
@router.get("/")
def get_schedules(
    skip: int = 0,           # Paginación: saltar registros
    limit: int = 100,        # Paginación: límite de registros
    semester: Optional[str] = None,  # Filtro por semestre
    teacher_id: Optional[int] = None,  # Filtro por profesor
    subject_id: Optional[int] = None,  # Filtro por asignatura
    db: Session = Depends(get_db)
):
    query = db.query(Schedule)
    
    # Aplicar filtros dinámicamente
    if semester:
        query = query.filter(Schedule.semester == semester)
    
    if teacher_id:
        query = query.filter(Schedule.teacher_id == teacher_id)
    
    if subject_id:
        query = query.filter(Schedule.subject_id == subject_id)
    
    # Aplicar paginación
    schedules = query.offset(skip).limit(limit).all()
    return schedules
```

### Manejo de Errores

```python
from fastapi import HTTPException, status

@router.get("/{schedule_id}")
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    
    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Horario no encontrado"
        )
    
    return schedule
```

---

## 🔒 Validaciones de Negocio

### Validación de Conflictos de Horario

```python
def check_schedule_conflicts(db: Session, schedule: ScheduleCreate):
    """Verificar conflictos de horario para aula y profesor"""
    
    # Verificar conflictos de horario para el aula
    conflicting_schedule = db.query(Schedule).filter(
        and_(
            Schedule.classroom_id == schedule.classroom_id,
            Schedule.day_of_week == schedule.day_of_week,
            Schedule.semester == schedule.semester,
            Schedule.is_active == True,
            or_(
                # Caso 1: El horario existente empieza antes y termina después del inicio del nuevo
                and_(Schedule.start_time <= schedule.start_time, 
                     Schedule.end_time > schedule.start_time),
                # Caso 2: El horario existente empieza antes del fin del nuevo y termina después
                and_(Schedule.start_time < schedule.end_time, 
                     Schedule.end_time >= schedule.end_time),
                # Caso 3: El horario existente está completamente dentro del nuevo
                and_(Schedule.start_time >= schedule.start_time, 
                     Schedule.end_time <= schedule.end_time)
            )
        )
    ).first()
    
    if conflicting_schedule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conflicto de horario: el aula ya está ocupada en este horario"
        )
```

### Lógica de Validación

#### 1. **Validación de Existencia**
```python
# Verificar que la asignatura existe
subject = db.query(Subject).filter(Subject.id == schedule.subject_id).first()
if not subject:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Asignatura no encontrada"
    )
```

#### 2. **Validación de Integridad Referencial**
```python
# Verificar que todas las entidades relacionadas existen
entities_to_check = [
    (Subject, schedule.subject_id, "Asignatura"),
    (ClassType, schedule.class_type_id, "Tipo de clase"),
    (Classroom, schedule.class