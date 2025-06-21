from fastapi import APIRouter
from app.api.v1.endpoints import subjects, teachers, class_types, classrooms, schedules

api_router = APIRouter()

api_router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
api_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
api_router.include_router(class_types.router, prefix="/class-types", tags=["class-types"])
api_router.include_router(classrooms.router, prefix="/classrooms", tags=["classrooms"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["schedules"]) 