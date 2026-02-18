"""
Smart AI Gym Coach - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.api.auth import router as auth_router
from src.api.profile import router as profile_router
from src.api.workouts import router as workouts_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Coach deportivo inteligente basado en LLM",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(workouts_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Smart AI Gym Coach API",
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check for monitoring"""
    return {"status": "healthy"}
