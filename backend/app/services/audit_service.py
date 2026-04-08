import json
from openai import OpenAI  # type: ignore
from ..core.config import settings


MODERN_TECH_BENCHMARK = """
MODERN INDUSTRY BENCHMARKS (2024-2025):
- Frontend: React/Next.js, TypeScript, Tailwind CSS, Vite
- Backend: FastAPI/Django/Node.js/Express, PostgreSQL, Redis
- DevOps: Docker, CI/CD (GitHub Actions), Cloud (AWS/GCP/Vercel)
- Testing: pytest, Jest, unit + integration tests
- Clean Code: Modular architecture, env-based config, linting, proper README
- Version Control: Branching strategy, meaningful commits, .gitignore
- APIs: REST (documented) or GraphQL
- Modern Stack combos: MERN, FastAPI+React, Django REST+React
"""

CAREER_LEVELS = """
CAREER LEVEL DEFINITIONS:
- "Learner": < 5 repos, basic HTML/CSS/JS, no architecture, tutorial-following
- "Fresher": 5-10 repos, knows a language well, some projects, no deployment/tests
- "Junior Developer": 10+ repos, uses frameworks, understands APIs, some structure, deployable apps
- "Mid-Level Developer": strong architecture, testing awareness, multiple stacks, some OSS
- "Senior Developer": production-grade, tests, CI/CD, clean architecture, OSS contributions, team patterns
"""

CODE_LEVELS = """
CODE QUALITY LEVELS:
- "Beginning": Messy, no structure, copy-paste, no config management, no README
- "Moderate": Some structure, basic docs, minimal tests, single-stack
- "Advanced": Modular, documented, env-based config, multi-stack, some testing
- "Professional": Production-grade, full test suites, CI/CD, scalable architecture, OSS-level quality
"""

PROJECT_READINESS = """
PROJECT JOB-READINESS LEVELS:
- "Not ready for internship/job": Only tutorial clones, no original ideas, incomplete projects
- "Internship ready": 2-3 original projects with README, basic CRUD apps, some deployment
- "Junior job ready": 3+ original projects, deployed, documented, show problem-solving
- "Job ready (mid-level+)": Complex projects, clean architecture, tests, real-world data, deployment
"""


class AuditService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.client = (
            OpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")
            if self.api_key
            else None
        )

    def perform_audit(self, github_data: dict) -> dict:
        if not self.client:
            return {"status": "error", "detail": "GROQ_API_KEY Missing"}

        username = github_data.get("login", "unknown")
        languages = github_data.get("languages", [])
        repo_summaries = github_data.get("repo_summaries", [])
        readme = github_data.get("readme", "")
        recent_commits = github_data.get("recent_commits", [])
        activity_level = github_data.get("activity_level", "Unknown")
        total_contributions = github_data.get("total_contributions_last_year", 0)
        total_commits = github_data.get("total_commits", 0)
        oss_pr_count = github_data.get("oss_pr_count", 0)
        oss_repos = github_data.get("oss_repos", [])
        top_repo_names = github_data.get("top_repo_names", [])
        active_weeks = github_data.get("active_weeks", 0)
        total_public_repos = github_data.get("total_public_repos", 0)

        prompt = f"""
You are a Staff Engineer performing a rigorous, brutally honest GitHub profile audit for '{username}'.

CONTEXT:
- Languages: {languages}
- Total Public Repos: {total_public_repos}
- Contributions last year: {total_contributions} (commits: {total_commits}, active weeks: {active_weeks})
- Activity Level: {activity_level}
- Open Source PRs (to OTHER repos): {oss_pr_count} in repos: {oss_repos or 'None'}
- Top 3 Repos: {top_repo_names}
- Repo summaries: {json.dumps(repo_summaries, indent=2)[:2000]}
- Latest README excerpt: {readme[:1000] or 'No README found'}
- Recent commit messages: {recent_commits}

{MODERN_TECH_BENCHMARK}
{CAREER_LEVELS}
{CODE_LEVELS}
{PROJECT_READINESS}

TASK:
Be STRICT and REALISTIC. Do NOT flatter. Only use "Senior" or "Professional" for genuinely production-grade profiles.
Evaluate based on what you see in repos, languages, commit patterns, and structure.

For "open_source_summary":
- If oss_pr_count > 0: list the repos contributed to
- If 0: write "No visible open source contributions, but has worked on personal projects showcasing problem-solving skills"

For "activity_summary":
- Use the activity_level and contribution counts. Example: "Low activity — {total_contributions} contributions in the past year across {active_weeks} active weeks. Commits occasionally."

RETURN ONLY VALID JSON:
{{
    "profile_career_level": "<Learner|Fresher|Junior Developer|Mid-Level Developer|Senior Developer>",
    "code_quality_label": "<Beginning|Moderate|Advanced|Professional>",
    "project_job_readiness": "<Not ready for internship/job|Internship ready|Junior job ready|Job ready (mid-level+)>",
    "subscores": {{
        "code_quality": <0-100>,
        "architecture": <0-100>,
        "engineering_practices": <0-100>,
        "project_depth": <0-100>,
        "problem_solving": <0-100>
    }},
    "technologies_used": ["list", "of", "actual", "tools"],
    "top_3_repos": ["{username}/repo1", "{username}/repo2", "{username}/repo3"],
    "open_source_summary": "...",
    "activity_summary": "...",
    "strengths": ["...", "..."],
    "skill_gaps": ["...", "..."],
    "insights": "2-3 sentence honest AI audit with specific actionable advice.",
    "mentor_match": "Best mentor archetype job title, e.g. Senior Backend Engineer"
}}
"""

        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        analysis = json.loads(completion.choices[0].message.content)

        # Calculate Weighted Maturity Score (0–10)
        sub = analysis.get("subscores", {})
        score_raw = (
            0.25 * sub.get("code_quality", 50)
            + 0.20 * sub.get("architecture", 50)
            + 0.20 * sub.get("engineering_practices", 50)
            + 0.20 * sub.get("project_depth", 50)
            + 0.15 * sub.get("problem_solving", 50)
        )
        analysis["maturity_score"] = float(f"{(score_raw / 10.0):.1f}")

        return analysis


# Singleton instance
audit_service = AuditService()
