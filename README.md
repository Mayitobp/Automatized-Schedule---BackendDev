# Sistema de Gestión de Horarios Académicos CUJAE

Un microservicio desarrollado con FastAPI, SQLAlchemy y PostgreSQL para la gestión automatizada de horarios académicos de la CUJAE.

## 🚀 Características

- **Gestión de Asignaturas**: Crear, editar y gestionar asignaturas con sus códigos y siglas
- **Gestión de Profesores**: Administrar profesores con información de contacto
- **Tipos de Clase**: Configurar diferentes tipos de clases (Conferencias, Laboratorios, Prácticas, etc.)
- **Gestión de Aulas**: Administrar aulas con capacidad y ubicación
- **Horarios Inteligentes**: Crear horarios con validación de conflictos
- **Exportación a Excel**: Generar horarios semanales y por profesor
- **API REST**: Interfaz completa para integración con otros sistemas

## 🛠️ Tecnologías

- **Backend**: FastAPI (Python)
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Validación**: Pydantic
- **Migraciones**: Alembic
- **Exportación**: OpenPyXL

## 📋 Requisitos Previos

- Python 3.8+
- PostgreSQL 12+
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd cujae-calendar-ms
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

1. Crear una base de datos PostgreSQL:
```sql
CREATE DATABASE cujae_calendar_db;
```

2. Copiar el archivo de configuración:
```bash
cp env.example .env
```

3. Editar `.env` con tus credenciales de base de datos:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/cujae_calendar_db
```

### 5. Ejecutar migraciones

```bash
alembic upgrade head
```

### 6. Inicializar datos de ejemplo (opcional)

```bash
python scripts/init_db.py
```

## 🚀 Ejecución

### Desarrollo

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 Documentación de la API

Una vez ejecutado el servidor, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔌 Endpoints Principales

### Asignaturas
- `GET /api/v1/subjects/` - Listar asignaturas
- `POST /api/v1/subjects/` - Crear asignatura
- `GET /api/v1/subjects/{id}` - Obtener asignatura
- `PUT /api/v1/subjects/{id}` - Actualizar asignatura
- `DELETE /api/v1/subjects/{id}` - Eliminar asignatura

### Profesores
- `GET /api/v1/teachers/` - Listar profesores
- `POST /api/v1/teachers/` - Crear profesor
- `GET /api/v1/teachers/{id}` - Obtener profesor
- `PUT /api/v1/teachers/{id}` - Actualizar profesor
- `DELETE /api/v1/teachers/{id}` - Eliminar profesor

### Tipos de Clase
- `GET /api/v1/class-types/` - Listar tipos de clase
- `POST /api/v1/class-types/` - Crear tipo de clase
- `GET /api/v1/class-types/{id}` - Obtener tipo de clase
- `PUT /api/v1/class-types/{id}` - Actualizar tipo de clase
- `DELETE /api/v1/class-types/{id}` - Eliminar tipo de clase

### Aulas
- `GET /api/v1/classrooms/` - Listar aulas
- `POST /api/v1/classrooms/` - Crear aula
- `GET /api/v1/classrooms/{id}` - Obtener aula
- `PUT /api/v1/classrooms/{id}` - Actualizar aula
- `DELETE /api/v1/classrooms/{id}` - Eliminar aula

### Horarios
- `GET /api/v1/schedules/` - Listar horarios
- `POST /api/v1/schedules/` - Crear horario
- `GET /api/v1/schedules/{id}` - Obtener horario
- `PUT /api/v1/schedules/{id}` - Actualizar horario
- `DELETE /api/v1/schedules/{id}` - Eliminar horario

### Exportación
- `GET /api/v1/schedules/export/weekly/{semester}` - Exportar horario semanal
- `GET /api/v1/schedules/export/teacher/{teacher_id}/{semester}` - Exportar horario por profesor

## 📊 Ejemplos de Uso

### Crear una asignatura

```bash
curl -X POST "http://localhost:8000/api/v1/subjects/" \
     -H "Content-Type: application/json" \
     -d '{
       "code": "INF103",
       "name": "Estructuras de Datos",
       "acronym": "ED",
       "description": "Algoritmos y estructuras de datos",
       "credits": 4
     }'
```

### Crear un horario

```bash
curl -X POST "http://localhost:8000/api/v1/schedules/" \
     -H "Content-Type: application/json" \
     -d '{
       "subject_id": 1,
       "class_type_id": 1,
       "classroom_id": 1,
       "teacher_id": 1,
       "day_of_week": 0,
       "start_time": "08:00",
       "end_time": "10:00",
       "semester": "2024-1",
       "week_start": "2024-02-05",
       "week_end": "2024-06-28"
     }'
```

### Exportar horario semanal

```bash
curl -X GET "http://localhost:8000/api/v1/schedules/export/weekly/2024-1" \
     --output horario_semanal_2024-1.xlsx
```

## 🗄️ Estructura de la Base de Datos

### Tablas Principales

- **subjects**: Asignaturas con código, nombre, siglas y créditos
- **teachers**: Profesores con información de contacto
- **class_types**: Tipos de clase (Conferencia, Laboratorio, etc.)
- **classrooms**: Aulas con capacidad y ubicación
- **schedules**: Horarios con validación de conflictos
- **subject_teachers**: Relación muchos a muchos entre asignaturas y profesores

### Relaciones

- Una asignatura puede tener múltiples profesores
- Un profesor puede enseñar múltiples asignaturas
- Un horario está asociado a una asignatura, profesor, tipo de clase y aula
- Se valida que no haya conflictos de horario para aulas y profesores

## 🔒 Validaciones

- **Conflictos de Horario**: El sistema verifica que no haya solapamiento de horarios para aulas y profesores
- **Integridad Referencial**: Todas las relaciones están protegidas con claves foráneas
- **Datos Únicos**: Códigos de asignatura, IDs de empleado y emails son únicos
- **Soft Delete**: Los registros se marcan como inactivos en lugar de eliminarse físicamente

## 🚀 Despliegue

### Docker (Recomendado)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variables de Entorno de Producción

```env
DATABASE_URL=postgresql://user:password@host:port/database
DEBUG=False
SECRET_KEY=your-secure-secret-key
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas, contacta a:
- Email: soporte@cujae.edu.cu
- Documentación: http://localhost:8000/docs

---

**Desarrollado para la CUJAE** 🎓 