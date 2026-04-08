import os
from pathlib import Path
from fastapi import FastAPI, Request # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from .api.endpoints import audit_api
from .db import database
from .core.config import settings

# 1. Initialize DB
database.init_db()

# 2. Setup App (API ONLY)
app = FastAPI(
    title=settings.PROJECT_NAME, 
    description="The engine powering MentorIQ coding analysis.",
    docs_url="/api/docs", 
    redoc_url="/api/redoc"
)

# 3. CORS - CRITICAL for Netlify to call Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with ["https://mentorqi1.netlify.app"] for security
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Success check for root
@app.get("/")
def read_root():
    return {
        "name": "MentorIQ API",
        "status": "online",
        "docs": "/api/docs"
    }

# 5. API Routes
app.include_router(audit_api.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
