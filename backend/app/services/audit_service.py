import json
from typing import List, Optional
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
import httpx
import instructor
from ..core.config import settings
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = structlog.get_logger()

# Structured Response Model for Instructor
class AuditSubscores(BaseModel):
    code_quality: int = Field(..., ge=0, le=100)
    architecture: int = Field(..., ge=0, le=100)
    engineering_practices: int = Field(..., ge=0, le=100)
    project_depth: int = Field(..., ge=0, le=100)
    problem_solving: int = Field(..., ge=0, le=100)

class AuditResponse(BaseModel):
    profile_career_level: str = Field(..., description="Learner|Fresher|Junior Developer|Mid-Level Developer|Senior Developer")
    code_quality_label: str = Field(..., description="Beginning|Moderate|Advanced|Professional")
    project_job_readiness: str = Field(..., description="Not ready for internship/job|Internship ready|Junior job ready|Job ready (mid-level+)")
    subscores: AuditSubscores
    technologies_used: List[str]
    top_3_repos: List[str]
    open_source_summary: str
    activity_summary: str
    strengths: List[str]
    skill_gaps: List[str]
    insights: str
    mentor_match: str

MODERN_TECH_BENCHMARK = """
MODERN INDUSTRY BENCHMARKS (2024-2025):
- Frontend: React/Next.js, TypeScript, Tailwind CSS, Vite
- Backend: FastAPI/Django/Node.js/Express, PostgreSQL, Redis
- DevOps: Docker, CI/CD (GitHub Actions), Cloud (AWS/GCP/Vercel)
- Testing: pytest, Jest, unit + integration tests ...
"""

class AuditService:
    def __init__(self):
        base_url = "https://api.groq.com/openai/v1" if settings.GROQ_API_KEY else None
        self.client = instructor.patch(AsyncOpenAI(
            api_key=settings.GROQ_API_KEY, 
            base_url=base_url
        )) if settings.GROQ_API_KEY else None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError, Exception)),
        reraise=True
    )
    async def perform_audit(self, github_data: dict) -> dict:
        if not self.client:
            logger.error("audit_service_unavailable", reason="Missing GROQ_API_KEY")
            return {"status": "error", "detail": "GROQ_API_KEY Missing"}

        username = github_data.get("login", "unknown")
        
        prompt = f"""
        Staff Engineer Audit for GitHub user: {username}
        Data: {json.dumps(github_data, indent=2)[:4000]}
        
        Benchmark Context:
        {MODERN_TECH_BENCHMARK}
        
        Task: Provide a brutally honest, evidence-based engineering audit. 
        Only award 'Senior' or 'Professional' for exceptional production-grade work.
        """

        try:
            analysis: AuditResponse = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                response_model=AuditResponse,
                messages=[{"role": "user", "content": prompt}],
            )
            
            # Convert to dict and calculate maturity score
            result = analysis.model_dump()
            sub = result["subscores"]
            score_raw = (
                0.25 * sub["code_quality"]
                + 0.20 * sub["architecture"]
                + 0.20 * sub["engineering_practices"]
                + 0.20 * sub["project_depth"]
                + 0.15 * sub["problem_solving"]
            )
            result["maturity_score"] = float(f"{(score_raw / 10.0):.1f}")
            result["status"] = "success"
            return result

        except Exception as e:
            logger.error("audit_computation_failed", username=username, error=str(e))
            return {"status": "error", "detail": str(e)}

audit_service = AuditService()
