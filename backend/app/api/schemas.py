from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Subscores(BaseModel):
    code_quality: int
    architecture: int
    engineering_practices: int
    project_depth: int
    problem_solving: int

class MatchedMentor(BaseModel):
    name: str
    job_title: str
    bio: str
    skills: List[str]

class AuditResult(BaseModel):
    status: str
    username: str
    avatar_url: str
    maturity_score: float
    subscores: Subscores
    profile_career_level: str
    code_quality_label: str
    project_job_readiness: str
    activity_level: str
    total_contributions: int
    active_weeks: int
    activity_overview: str
    oss_pr_count: int
    oss_repos: List[str]
    open_source_contributions: str
    technologies_used: List[str]
    top_3_repos: List[str]
    strengths: List[str]
    skill_gaps: List[str]
    insights: str
    mentor_match: str
    matched_mentor: Optional[MatchedMentor] = None
