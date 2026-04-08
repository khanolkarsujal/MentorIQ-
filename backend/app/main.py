import os
from pathlib import Path
from fastapi import FastAPI, Request # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi.responses import FileResponse # type: ignore
from .api.endpoints import audit_api
from .db import database
from .core.config import settings

# 1. Initialize DB
database.init_db()

# 2. Setup App
app = FastAPI(title=settings.PROJECT_NAME, docs_url="/api/docs", redoc_url="/api/redoc")

# 3. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Paths
BASE_DIR = Path(__file__).resolve().parent.parent # /app in Docker or backend/ locally
if (BASE_DIR / "frontend").exists():
    PROJECT_ROOT = BASE_DIR
else:
    PROJECT_ROOT = BASE_DIR.parent
frontend_dist = PROJECT_ROOT / "frontend" / "dist"
frontend_dev = PROJECT_ROOT / "frontend"
frontend_path = frontend_dist if frontend_dist.exists() else frontend_dev

# Mount /frontend path for static assets (logo, images referenced as /frontend/images/...)
frontend_images = frontend_path / "frontend"
if frontend_images.exists():
    app.mount("/frontend", StaticFiles(directory=str(frontend_images)), name="frontend-assets")

# 5. API Routes (must be before static file catch-all)
app.include_router(audit_api.router, prefix=settings.API_V1_STR)

# 6. Serve index.html for root and all non-API routes (SPA support)
index_html = frontend_path / "index.html"

@app.get("/")
async def serve_home():
    return FileResponse(str(index_html))

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Catch-all: serve index.html for client-side routing."""
    # Don't intercept API or asset paths
    if full_path.startswith("api/") or full_path.startswith("frontend/"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404)
    return FileResponse(str(index_html))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

