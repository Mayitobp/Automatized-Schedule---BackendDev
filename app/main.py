from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.api import api_router
from app.database import engine
from app.models import *  # Import all models

# Create database tables
def create_tables():
    """Create all database tables"""
    from app.database import Base
    Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Sistema de Gestión de Horarios Académicos CUJAE",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    create_tables()

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "CUJAE Calendar Management System is running"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Bienvenido al Sistema de Gestión de Horarios Académicos CUJAE",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    } 