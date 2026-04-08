import re
from fastapi import APIRouter, Query, HTTPException  # type: ignore
from ...services.github_service import GitHubService
from ...services.audit_service import audit_service
from ...db import database

router = APIRouter()


@router.get("/analyze")
async def analyze_github(username: str = Query(..., min_length=1)):
    # 1. Sanitize
    username = re.sub(r"[^a-zA-Z0-9\-.]", "", username)
    if len(username) > 39:
        raise HTTPException(status_code=400, detail="Username too long.")

    # 2. Fetch all data via GitHub GraphQL (single call)
    try:
        github_data = GitHubService.fetch_profile_data(username)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if not github_data.get("top_repo_names"):
        raise HTTPException(status_code=404, detail="No public repositories found.")

    # 3. Perform AI Audit with rich context
    analysis = audit_service.perform_audit(github_data)

    if analysis.get("status") == "error":
        raise HTTPException(status_code=500, detail=analysis.get("detail"))

    # 4. Mentor Matchmaking
    mentor_job = analysis.get("mentor_match", "")
    user_tools = analysis.get("technologies_used", [])
    matched = database.find_best_mentors(mentor_job, user_tools)
    
    matched_mentor = None
    if matched:
        m = matched[0]
        matched_mentor = {
            "name": m["name"],
            "job_title": f"{m['title']} at {m['company']}",
            "bio": f"Expert in {', '.join(m['tech_stack'][:3])}. Currently leading engineering efforts at {m['company']}. Highly experienced in navigating career growth in top-tier tech companies.",
            "skills": m["tech_stack"]
        }

    career = analysis.get("profile_career_level") or analysis.get("github_profile_level") or "Unknown"
    code_label = analysis.get("code_quality_label") or analysis.get("coding_skills_level") or "Unknown"
    project_ready = analysis.get("project_job_readiness") or analysis.get("project_quality_level") or "Unknown"
    oss_summary = analysis.get("open_source_summary") or analysis.get("open_source_contributions") or ""
    act_summary = analysis.get("activity_summary") or analysis.get("activity_overview") or ""
    subscores = analysis.get("subscores", {})

    return {
        "status": "success",
        "username": username,
        "avatar_url": f"https://github.com/{username}.png",
        "maturity_score": analysis.get("maturity_score", 0),
        "subscores": subscores,
        "profile_career_level": career,
        "code_quality_label": code_label,
        "project_job_readiness": project_ready,
        "activity_level": github_data.get("activity_level", "Unknown"),
        "total_contributions": github_data.get("total_contributions_last_year", 0),
        "active_weeks": github_data.get("active_weeks", 0),
        "activity_overview": act_summary,
        "oss_pr_count": github_data.get("oss_pr_count", 0),
        "oss_repos": github_data.get("oss_repos", []),
        "open_source_contributions": oss_summary,
        "technologies_used": analysis.get("technologies_used", github_data.get("languages", [])),
        "top_3_repos": analysis.get("top_3_repos", github_data.get("top_repo_names", [])),
        "strengths": analysis.get("strengths", []),
        "skill_gaps": analysis.get("skill_gaps", []),
        "insights": analysis.get("insights", ""),
        "mentor_match": analysis.get("mentor_match", ""),
        "matched_mentor": matched_mentor,
    }


@router.get("/status")
def get_status():
    return {"status": "online", "api_v": "v2.0-graphql"}
