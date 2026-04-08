import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import redis.asyncio as redis
from .api.endpoints import audit_api
from .db import database
from .core.config import settings
from .core.logging import setup_logging
from .services.cache_service import cache_service
import structlog

# 1. Setup Logging first
setup_logging()
logger = structlog.get_logger()

# 2. Lifespan manager (startup / shutdown / rate-limiter init)
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup", project=settings.PROJECT_NAME, env=settings.ENV)
    
    # Init DB
    database.init_db()
    
    logger.info("system_ready")
    yield
    
    # Close Redis global connection pool if it exists
    await cache_service.close()
    logger.info("shutdown")

# 3. App
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="The AI engine powering MentorIQ GitHub profile auditing.",
    version="3.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# 4. CORS & Security Headers Middleware
ALLOWED_ORIGINS = settings.ALLOWED_ORIGINS or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def security_headers_and_timing(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    
    # Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "http_request",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration_ms=elapsed_ms,
        client_ip=request.client.host if request.client else "unknown"
    )
    response.headers["X-Response-Time-Ms"] = str(elapsed_ms)
    return response

# 5. Global Exception Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("unhandled_exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "status": "error"}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("validation_error", errors=exc.errors(), path=request.url.path)
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid Request Parameters", "errors": exc.errors(), "status": "error"}
    )

# 6. Root health-check
@app.get("/", tags=["Health"])
async def read_root():
    return {
        "name": "MentorIQ API",
        "version": "3.0.0",
        "status": "online",
        "docs": "/api/docs",
    }

# 7. API Routes
app.include_router(audit_api.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
