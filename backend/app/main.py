"""
Main FastAPI application for Infinite Helix.
AI-Powered Medical Report Analysis Platform.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
from contextlib import asynccontextmanager
from datetime import datetime

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.database import init_db, close_db
from app.routers import upload, analyze, results, auth, translate, chat, advanced, unified_ai, live_agent
from app.schemas import ErrorResponse, HealthCheckResponse

# Import Pathway and Live Agent services
from app.services.pathway_memory_service import initialize_pathway_memory
from app.services.live_adaptive_agent import initialize_live_agent

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    ENHANCED: Now initializes Pathway Live Memory and Live Adaptive Agent
    """
    # Startup
    logger.info("Starting Infinite Helix application...")
    logger.info("=" * 80)
    logger.info("🧬 LIVE ADAPTIVE MEDICAL INTELLIGENCE - PATHWAY ENABLED")
    logger.info("=" * 80)
    
    try:
        # Initialize database (PostgreSQL - durable storage)
        init_db()
        logger.info("✓ PostgreSQL database initialized (durable storage layer)")
    except Exception as e:
        logger.error(f"✗ Failed to initialize database: {str(e)}")
    
    try:
        # Initialize Pathway Live Memory (cognitive memory substrate)
        pathway_memory = initialize_pathway_memory()
        logger.info("✓ Pathway Live Memory initialized (cognitive memory layer)")
        logger.info(f"  - Patient docs: {pathway_memory.patient_docs_dir}")
        logger.info(f"  - Knowledge docs: {pathway_memory.knowledge_docs_dir}")
        logger.info(f"  - Streaming: {'enabled' if pathway_memory.patient_memory_table else 'fallback mode'}")
    except Exception as e:
        logger.error(f"✗ Pathway initialization failed: {str(e)}")
        logger.warning("  Agent will run without live memory features")
        pathway_memory = None
    
    try:
        # Initialize Live Adaptive Agent
        live_agent = initialize_live_agent(pathway_memory=pathway_memory)
        logger.info("✓ Live Adaptive Agent initialized")
        logger.info("  - Temporal reasoning: enabled")
        logger.info("  - LLM reasoning: enabled" if live_agent.groq_client else "  - LLM reasoning: disabled (no API key)")
        logger.info("  - BioBERT NER: enabled")
        logger.info("  - Anomaly detection: enabled")
    except Exception as e:
        logger.error(f"✗ Live Agent initialization failed: {str(e)}")
        logger.warning("  Falling back to base agent")
    
    logger.info("=" * 80)
    logger.info(f"Application started in {settings.environment} mode")
    logger.info("POST-TRANSFORMER INTELLIGENCE: Continuous Memory • Temporal Reasoning • Live Adaptation")
    logger.info("=" * 80)
    
    yield
    
    # Shutdown
    logger.info("Shutting down Infinite Helix application...")
    
    try:
        close_db()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-Powered Medical Report Analysis - Democratizing Healthcare Intelligence",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS - Allow frontend access
cors_origins = settings.allowed_origins if isinstance(settings.allowed_origins, list) else [settings.allowed_origins]
# Add common localhost origins for development
if settings.debug or settings.environment == "development":
    cors_origins.extend([
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ])
    # Remove duplicates
    cors_origins = list(set(cors_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors with detailed error messages.
    """
    logger.warning(f"Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="Validation Error",
            detail=str(exc.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal Server Error",
            detail="An unexpected error occurred. Please try again later." if not settings.debug else str(exc),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ).dict()
    )


# Include routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(results.router)
app.include_router(translate.router)
app.include_router(chat.router)
app.include_router(advanced.router)
app.include_router(unified_ai.router)  # ONE POWERFUL AI ENDPOINT
app.include_router(live_agent.router)  # 🚀 NEW: LIVE ADAPTIVE AGENT ENDPOINTS

# Mount static files (frontend)
# Get the frontend directory path
frontend_dir = Path(__file__).parent.parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")
    logger.info(f"Mounted frontend static files from: {frontend_dir}")


# Serve index.html at root
@app.get(
    "/",
    tags=["frontend"],
    summary="Frontend Home",
    description="Serve the main frontend application"
)
async def serve_frontend():
    """
    Serve the frontend index.html
    """
    frontend_file = Path(__file__).parent.parent.parent / "frontend" / "index.html"
    if frontend_file.exists():
        return FileResponse(frontend_file)
    else:
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "description": "AI-Powered Medical Report Analysis Platform",
            "documentation": "/docs" if settings.debug else "Contact administrator",
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat()
        }


# API Root endpoint
@app.get(
    "/api",
    tags=["health"],
    summary="API Root",
    description="Welcome endpoint with API information"
)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def root(request: Request):
    """
    Root endpoint providing API information.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "AI-Powered Medical Report Analysis Platform",
        "documentation": "/docs" if settings.debug else "Contact administrator",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }


# Health check endpoint
@app.get(
    "/health",
    response_model=HealthCheckResponse,
    tags=["health"],
    summary="Health Check",
    description="Check API health and service status"
)
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    # Check database connectivity
    db_healthy = True
    try:
        from app.database import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_healthy = False
    
    # Check services
    services_status = {
        "ocr": True,  # Could add actual OCR check
        "nlp": True,  # Could add actual NLP model check
    }
    
    return HealthCheckResponse(
        status="healthy" if db_healthy else "unhealthy",
        version=settings.app_version,
        database=db_healthy,
        services=services_status
    )


# Metrics endpoint (for monitoring)
@app.get(
    "/metrics",
    tags=["monitoring"],
    summary="Application Metrics",
    description="Get application metrics for monitoring"
)
async def metrics():
    """
    Return application metrics.
    """
    from app.database import SessionLocal
    from app.models import UploadedFile, Analysis
    
    try:
        db = SessionLocal()
        
        total_uploads = db.query(UploadedFile).count()
        total_analyses = db.query(Analysis).count()
        completed_analyses = db.query(Analysis).filter(
            Analysis.status == "completed"
        ).count()
        failed_analyses = db.query(Analysis).filter(
            Analysis.status == "failed"
        ).count()
        
        db.close()
        
        return {
            "total_uploads": total_uploads,
            "total_analyses": total_analyses,
            "completed_analyses": completed_analyses,
            "failed_analyses": failed_analyses,
            "success_rate": f"{(completed_analyses / total_analyses * 100):.2f}%" if total_analyses > 0 else "0%",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}")
        return {
            "error": "Unable to retrieve metrics",
            "timestamp": datetime.utcnow().isoformat()
        }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
