from contextlib import asynccontextmanager
import logging

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import setup_logging
from app.middleware.logging_middleware import LoggingMiddleware

from app.config.config import settings


# --------------------------------
# Setup Logging
# --------------------------------
setup_logging()
logger = logging.getLogger(__name__)


# --------------------------------
# Application Lifespan
# --------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Event Management System...")

    # Initialize resources here
    # await connect_db()
    # await redis.connect()

    yield

    logger.info("🛑 Shutting down Event Management System")

    # Cleanup resources here
    # await disconnect_db()
    # await redis.disconnect()


# --------------------------------
# Create FastAPI App
# --------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend for Event Management System",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# --------------------------------
# Middleware
# --------------------------------
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------
# API Router
# --------------------------------
from app.routes.auth.register import router as auth_router


api_router = APIRouter(prefix=settings.API_PREFIX)
api_router.include_router(auth_router)

# --------------------------------
# Health Check Endpoint
# --------------------------------
@api_router.get(
    "/health",
    tags=["Health"],
    summary="Health Check"
)
async def health_check():
    logger.info("Health check endpoint called")

    return {
        "status": "healthy",
        "service": "Event Management System API",
        "application_environment": settings.APP_ENV
    }


# --------------------------------
# Root Endpoint
# --------------------------------
@api_router.get(
    "/",
    tags=["Root"],
    summary="Root Endpoint for the Backend Service."
)
async def root():
    logger.info("Root endpoint called !")

    return {
        "status": "ok",
        "message": "Welcome to the Event Management System",
        "service": "Event Management System",
        "application_environment": settings.APP_ENV,
    }

# API Router
app.include_router(api_router)

