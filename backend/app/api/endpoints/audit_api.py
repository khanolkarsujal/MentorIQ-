import re
from fastapi import APIRouter, Query, HTTPException, Depends, Request
from ...services.github_service import GitHubService
from ...services.audit_service import audit_service
from ...services.cache_service import cache_service
from ...db import database
from ..schemas import AuditResult, MatchedMentor
import structlog

logger = structlog.get_logger()
router = APIRouter()

@router.get("/analyze", response_model=AuditResult)
async def analyze_github(request: Request, username: str = Query(..., min_length=1)):
    """Perform a deep AI audit of a GitHub profile."""
    # 0. Rate Limiting (30 requests per minute)
    ip = request.client.host if request.client else "127.0.0.1"
    allowed = await cache_service.rate_limit(ip, limit=30, window=60)
    if not allowed:
        logger.warning("rate_limit_exceeded", ip=ip)
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")

    # 1. Sanitize
    username = re.sub(r"[^a-zA-Z0-9\-.]", "", username)
    if len(username) > 39:
        raise HTTPException(status_code=400, detail="Username too long.")

    log = logger.bind(username=username)
    log.info("analysis_started")
    
    # 1.5. Check Cache
    cached_result = await cache_service.get_analysis(username)
    if cached_result:
        return AuditResult(**cached_result)

    # 2. Fetch Data (Async)
    try:
        github_data = await GitHubService.fetch_profile_data(username)
    except ValueError as e:
        log.error("github_data_fetch_failed", error=str(e))
        raise HTTPException(status_code=404, detail=str(e))

    if not github_data.get("top_repo_names") and github_data.get("data_source") != "mock":
        raise HTTPException(status_code=404, detail="No public repositories found.")

    # 3. Perform AI Audit (Async)
    analysis = await audit_service.perform_audit(github_data)
    if analysis.get("status") == "error":
        log.error("audit_failed", error=analysis.get("detail"))
        raise HTTPException(status_code=500, detail=analysis.get("detail"))

    # 4. Mentor Matchmaking
    mentor_job = analysis.get("mentor_match", "")
    user_tools = analysis.get("technologies_used", [])
    matched_mentors = database.find_best_mentors(mentor_job, user_tools)
    
    matched_mentor = None
    if matched_mentors:
        m = matched_mentors[0]
        matched_mentor = MatchedMentor(
            name=m["name"],
            job_title=f"{m['title']} at {m['company']}",
            bio=f"Expert in {', '.join(m['tech_stack'][:3])}. Currently leading engineering efforts at {m['company']}. Highly experienced in navigating career growth in top-tier tech companies.",
            skills=m["tech_stack"]
        )

    log.info("analysis_completed", score=analysis.get("maturity_score"))

    result = AuditResult(
        status="success",
        username=username,
        avatar_url=f"https://github.com/{username}.png",
        maturity_score=analysis.get("maturity_score", 0),
        subscores=analysis.get("subscores"),
        profile_career_level=analysis.get("profile_career_level", "Unknown"),
        code_quality_label=analysis.get("code_quality_label", "Unknown"),
        project_job_readiness=analysis.get("project_job_readiness", "Unknown"),
        activity_level=github_data.get("activity_level", "Unknown"),
        total_contributions=github_data.get("total_contributions_last_year", 0),
        active_weeks=github_data.get("active_weeks", 0),
        activity_overview=analysis.get("activity_summary", ""),
        oss_pr_count=github_data.get("oss_pr_count", 0),
        oss_repos=github_data.get("oss_repos", []),
        open_source_contributions=analysis.get("open_source_summary", ""),
        technologies_used=analysis.get("technologies_used", []),
        top_3_repos=analysis.get("top_3_repos", []),
        strengths=analysis.get("strengths", []),
        skill_gaps=analysis.get("skill_gaps", []),
        insights=analysis.get("insights", ""),
        mentor_match=analysis.get("mentor_match", ""),
        matched_mentor=matched_mentor
    )
    
    # 5. Save to Cache
    await cache_service.set_analysis(username, result.model_dump())
    
    return result

@router.get("/status")
async def get_status():
    return {"status": "online", "api_v": "v3.0-async"}
