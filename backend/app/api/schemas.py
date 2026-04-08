from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Subscores(BaseModel):
    code_quality: int = Field(..., description="Score for logic, naming, and cleanliness (0-100)", ge=0, le=100)
    architecture: int = Field(..., description="Score for structure, modularity, and patterns (0-100)", ge=0, le=100)
    engineering_practices: int = Field(..., description="Score for testing, docs, and Git usage (0-100)", ge=0, le=100)
    project_depth: int = Field(..., description="Score for technical complexity and domain depth (0-100)", ge=0, le=100)
    problem_solving: int = Field(..., description="Score for algorithm efficiency and logic (0-100)", ge=0, le=100)

class MatchedMentor(BaseModel):
    name: str = Field(..., description="Name of the matched mentor")
    job_title: str = Field(..., description="Current role and company of the mentor")
    bio: str = Field(..., description="Summary of the mentor's expertise and value")
    skills: List[str] = Field(..., description="List of technologies the mentor specializes in")

class AuditResult(BaseModel):
    status: str = Field(..., description="Success or error status")
    username: str = Field(..., description="GitHub username analyzed")
    avatar_url: str = Field(..., description="URL to user's GitHub avatar")
    maturity_score: float = Field(..., description="Overall score between 0.0 and 10.0")
    subscores: Subscores = Field(..., description="Detailed breakdown of scores across 5 categories")
    profile_career_level: str = Field(..., description="AI-assessed career level (e.g., Junior, Mid-Level)")
    code_quality_label: str = Field(..., description="Qualitative label for code quality")
    project_job_readiness: str = Field(..., description="Assessment of readiness for a professional role")
    activity_level: str = Field(..., description="Frequency of contributions label")
    total_contributions: int = Field(..., description="Total contributions in the last year")
    active_weeks: int = Field(..., description="Number of weeks with activity in the last year")
    activity_overview: str = Field(..., description="Summary of the user's activity habits")
    oss_pr_count: int = Field(..., description="Number of open source pull requests")
    oss_repos: List[str] = Field(..., description="Names of open source repositories contributed to")
    open_source_contributions: str = Field(..., description="Summary of OSS impact")
    technologies_used: List[str] = Field(..., description="Key technologies identified in profile")
    top_3_repos: List[str] = Field(..., description="Recommended repositories to highlight")
    strengths: List[str] = Field(..., description="Key technical strengths")
    skill_gaps: List[str] = Field(..., description="Areas for improvement")
    insights: str = Field(..., description="Nuanced AI insights on the developer profile")
    mentor_match: str = Field(..., description="Recommended mentor persona or area")
    matched_mentor: Optional[MatchedMentor] = Field(None, description="Actual mentor database match if found")
