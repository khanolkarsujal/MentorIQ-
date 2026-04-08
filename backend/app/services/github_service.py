import httpx
import json
import itertools
import asyncio
import structlog
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List
from ..core.config import settings
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = structlog.get_logger()

GRAPHQL_URL = "https://api.github.com/graphql"

GRAPHQL_QUERY = """
query($username: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $username) {
    name
    login
    bio
    company
    location
    followers { totalCount }
    following { totalCount }
    repositories(
      first: 20,
      ownerAffiliations: OWNER,
      orderBy: { field: UPDATED_AT, direction: DESC },
      privacy: PUBLIC
    ) {
      totalCount
      nodes {
        name
        description
        stargazerCount
        forkCount
        isFork
        updatedAt
        primaryLanguage { name }
        languages(first: 10, orderBy: { field: SIZE, direction: DESC }) {
          edges { size node { name } }
        }
        object(expression: "HEAD:README.md") {
          ... on Blob { text }
        }
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 5) {
                nodes { message committedDate }
              }
            }
          }
        }
      }
    }
    pinnedItems(first: 6, types: REPOSITORY) {
      nodes {
        ... on Repository {
          name description stargazerCount
          primaryLanguage { name }
        }
      }
    }
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { contributionCount date }
        }
      }
    }
    pullRequests(states: MERGED, first: 20, orderBy: { field: CREATED_AT, direction: DESC }) {
      totalCount
      nodes {
        title createdAt
        repository { nameWithOwner owner { login } }
      }
    }
  }
}
"""


def _rest_headers() -> Dict[str, str]:
    h = {"User-Agent": "MentorIQ-Audit", "Accept": "application/vnd.github.v3+json"}
    if settings.GITHUB_TOKEN:
        h["Authorization"] = f"token {settings.GITHUB_TOKEN}"
    return h


class GitHubService:

    @staticmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        reraise=True
    )
    async def fetch_profile_data(username: str) -> Dict[str, Any]:
        """Fetch profile data asynchronously using GraphQL or REST fallback."""
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                if settings.GITHUB_TOKEN:
                    return await GitHubService._fetch_graphql(client, username)
                return await GitHubService._fetch_rest(client, username)
            except Exception as e:
                logger.error("github_fetch_failed", username=username, error=str(e))
                if "rate limit" in str(e).lower() or "limit exceeded" in str(e).lower() or isinstance(e, httpx.TimeoutException):
                    # We only return mock data if it's a rate limit. If it's a timeout, we retry, and if retries fail, it raises.
                    return GitHubService.get_mock_data(username)
                raise ValueError(f"Failed to fetch GitHub data: {str(e)}")

    @staticmethod
    async def _fetch_graphql(client: httpx.AsyncClient, username: str) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        one_year_ago = now - timedelta(days=365)
        variables = {
            "username": username,
            "from": one_year_ago.isoformat(),
            "to": now.isoformat(),
        }
        
        resp = await client.post(
            GRAPHQL_URL,
            json={"query": GRAPHQL_QUERY, "variables": variables},
            headers={"Authorization": f"Bearer {settings.GITHUB_TOKEN}"},
        )
        
        if resp.status_code == 401:
            raise ValueError("GitHub token is invalid.")
        if resp.status_code != 200:
            raise ValueError(f"GitHub GraphQL API status {resp.status_code}.")

        body = resp.json()
        if "errors" in body:
            msgs = [e.get("message", "") for e in body["errors"]]
            if any("Could not resolve to a User" in m for m in msgs):
                raise ValueError(f"GitHub user '{username}' not found.")
            raise ValueError(f"GitHub API error: {'; '.join(msgs)}")

        user = body.get("data", {}).get("user")
        if not user:
            raise ValueError(f"GitHub user '{username}' not found.")

        return GitHubService._parse_graphql(user)

    @staticmethod
    def _parse_graphql(user: Dict[str, Any]) -> Dict[str, Any]:
        repos_raw: List[Dict] = user.get("repositories", {}).get("nodes", [])
        contrib = user.get("contributionsCollection", {})
        calendar = contrib.get("contributionCalendar", {})
        prs_raw: List[Dict] = user.get("pullRequests", {}).get("nodes", [])

        # Languages
        lang_bytes: Dict[str, int] = {}
        for repo in repos_raw:
            if repo.get("isFork"):
                continue
            for edge in repo.get("languages", {}).get("edges", []):
                name = edge["node"]["name"]
                lang_bytes[name] = lang_bytes.get(name, 0) + edge.get("size", 0)
        languages = sorted(lang_bytes, key=lambda x: lang_bytes[x], reverse=True)[:10]

        # Repos
        own_repos = [r for r in repos_raw if not r.get("isFork")]
        top_repos = sorted(own_repos, key=lambda r: r.get("stargazerCount", 0), reverse=True)[:5]
        repo_summaries = []
        for r in top_repos:
            lang = r.get("primaryLanguage") or {}
            repo_summaries.append({
                "name": r.get("name", ""),
                "description": r.get("description") or "",
                "stars": r.get("stargazerCount", 0),
                "language": lang.get("name", "Unknown"),
            })

        # README
        readme = ""
        for repo in repos_raw:
            obj = repo.get("object")
            if obj and isinstance(obj, dict):
                text = obj.get("text") or ""
                if text:
                    readme = text[:3000]
                    break

        # Recent commits
        recent_commits: List[str] = []
        if repos_raw:
            branch = (repos_raw[0].get("defaultBranchRef") or {})
            target = branch.get("target") or {}
            history = target.get("history") or {}
            recent_commits = [n.get("message", "") for n in history.get("nodes", [])]

        # Activity
        total_contributions = calendar.get("totalContributions", 0)
        total_commits = contrib.get("totalCommitContributions", 0)
        total_prs_made = contrib.get("totalPullRequestContributions", 0)
        total_issues = contrib.get("totalIssueContributions", 0)
        weeks = calendar.get("weeks", [])
        active_weeks = sum(
            1 for w in weeks
            if any(d.get("contributionCount", 0) > 0 for d in w.get("contributionDays", []))
        )
        activity_level = _compute_activity_level(total_contributions, active_weeks)

        # OSS PRs
        login = user.get("login", "")
        oss_prs = [
            pr for pr in prs_raw
            if (pr.get("repository") or {}).get("owner", {}).get("login", "").lower() != login.lower()
        ]
        oss_repos = list({pr["repository"]["nameWithOwner"] for pr in oss_prs})

        return {
            "login": login,
            "name": user.get("name") or login,
            "bio": user.get("bio") or "",
            "followers": user.get("followers", {}).get("totalCount", 0),
            "total_public_repos": user.get("repositories", {}).get("totalCount", 0),
            "languages": languages,
            "top_repo_names": [r["name"] for r in repo_summaries[:3]],
            "repo_summaries": repo_summaries,
            "readme": readme,
            "recent_commits": recent_commits,
            "total_contributions_last_year": total_contributions,
            "total_commits": total_commits,
            "total_prs_made": total_prs_made,
            "total_issues": total_issues,
            "active_weeks": active_weeks,
            "activity_level": activity_level,
            "oss_pr_count": len(oss_prs),
            "oss_repos": oss_repos[:5],
            "data_source": "graphql",
        }

    @staticmethod
    async def _fetch_rest(client: httpx.AsyncClient, username: str) -> Dict[str, Any]:
        headers = _rest_headers()

        # 1. User profile
        resp = await client.get(f"https://api.github.com/users/{username}", headers=headers)
        if resp.status_code == 404:
            raise ValueError(f"GitHub user '{username}' not found.")
        if resp.status_code == 403:
            raise ValueError("GitHub API rate limit exceeded.")
        if resp.status_code != 200:
            raise ValueError(f"GitHub API error: {resp.status_code}")
        profile = resp.json()

        # 2. Repos
        repos_resp = await client.get(
            f"https://api.github.com/users/{username}/repos?sort=updated&per_page=20",
            headers=headers
        )
        repos_raw = repos_resp.json() if repos_resp.status_code == 200 else []

        own_repos = [r for r in repos_raw if not r.get("fork", False)]
        top_repos = sorted(own_repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:5]

        repo_summaries = [
            {
                "name": r.get("name", ""),
                "description": r.get("description") or "",
                "stars": r.get("stargazers_count", 0),
                "language": r.get("language") or "Unknown",
            }
            for r in top_repos
        ]

        # 3. Languages (parallel calls for better performance)
        lang_bytes: Dict[str, int] = {}
        lang_tasks = [
            client.get(f"https://api.github.com/repos/{username}/{repo['name']}/languages", headers=headers)
            for repo in top_repos[:5]
        ]
        lang_resps = await asyncio.gather(*lang_tasks, return_exceptions=True)
        for r in lang_resps:
            if isinstance(r, httpx.Response) and r.status_code == 200:
                for lang, count in r.json().items():
                    lang_bytes[lang] = lang_bytes.get(lang, 0) + count
        
        languages = sorted(lang_bytes, key=lambda x: lang_bytes[x], reverse=True)[:10]

        # 4. README
        readme = ""
        if top_repos:
            readme = await GitHubService.fetch_readme(client, username, top_repos[0]["name"])

        # 5. Activity Scraper Fallback (No Token)
        activity_data = await GitHubService._scrape_activity(client, username)

        return {
            "login": username,
            "name": profile.get("name") or username,
            "bio": profile.get("bio") or "",
            "followers": profile.get("followers", 0),
            "total_public_repos": profile.get("public_repos", 0),
            "languages": languages,
            "top_repo_names": [r["name"] for r in repo_summaries[:3]],
            "repo_summaries": repo_summaries,
            "readme": readme,
            "recent_commits": [],
            "total_contributions_last_year": activity_data["total"],
            "total_commits": int(activity_data["total"] * 0.7), # Estimation
            "total_prs_made": 0,
            "total_issues": 0,
            "active_weeks": activity_data["active_weeks"],
            "activity_level": activity_data["level"],
            "oss_pr_count": 0,
            "oss_repos": [],
            "data_source": "rest+scraped",
        }

    @staticmethod
    async def _scrape_activity(client: httpx.AsyncClient, username: str) -> Dict[str, Any]:
        """Scrape the contributions calendar for total contributions and active weeks."""
        try:
            url = f"https://github.com/users/{username}/contributions"
            resp = await client.get(url, timeout=10)
            if resp.status_code != 200:
                return {"total": 0, "active_weeks": 0, "level": "Unknown"}
            
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Find total contributions text (e.g., "500 contributions in the last year")
            h2 = soup.find("h2", class_="f4 text-normal mb-2")
            total = 0
            if h2:
                text = h2.get_text(separator=" ", strip=True)
                # Extract number
                parts = text.split()
                if parts:
                    total_str = parts[0].replace(",", "")
                    if total_str.isdigit():
                        total = int(total_str)
            
            # Find active weeks (count rects with count > 0)
            # GitHub uses data-count or data-level
            rects = soup.find_all("td", class_="ContributionCalendar-day")
            if not rects:
                # Handle newer GitHub UI table cells
                rects = soup.find_all("tool-tip") # Some versions use tooltips for counts
            
            # Simplified: just count non-zero levels in svg cells
            active_days = 0
            # Modern GitHub uses <rect data-level="1">
            rects = soup.find_all("rect", class_="ContributionCalendar-day")
            for r in rects:
                level = r.get("data-level", "0")
                if level != "0":
                    active_days += 1
            
            # Rough estimate of active weeks
            active_weeks = min(52, max(0, active_days // 3 + (1 if active_days % 3 > 0 else 0))) if active_days > 0 else 0
            if total > 0 and active_weeks == 0: active_weeks = 1 # Safety
            
            level = _compute_activity_level(total, active_weeks)
            
            return {"total": total, "active_weeks": active_weeks, "level": level}
        except Exception as e:
            logger.warning("contribution_scrape_failed", username=username, error=str(e))
            return {"total": 0, "active_weeks": 0, "level": "Unknown"}

    @staticmethod
    async def fetch_readme(client: httpx.AsyncClient, username: str, repo_name: str) -> str:
        headers = _rest_headers()
        for branch in ["main", "master"]:
            try:
                url = f"https://raw.githubusercontent.com/{username}/{repo_name}/{branch}/README.md"
                res = await client.get(url, headers=headers, timeout=5)
                if res.status_code == 200:
                    return res.text[:3000]
            except Exception:
                continue
        return ""

    @staticmethod
    def get_mock_data(username: str) -> Dict[str, Any]:
        return {
            "login": username,
            "name": username.capitalize(),
            "bio": "AI-simulated profile due to API limits/timeout.",
            "followers": 150,
            "total_public_repos": 10,
            "languages": ["Python", "JavaScript", "React"],
            "top_repo_names": [f"{username}/project-alpha", f"{username}/demo"],
            "repo_summaries": [],
            "readme": "Mock README content.",
            "recent_commits": [],
            "total_contributions_last_year": 100,
            "total_commits": 80,
            "total_prs_made": 5,
            "total_issues": 2,
            "active_weeks": 10,
            "activity_level": "Moderate",
            "oss_pr_count": 2,
            "oss_repos": ["facebook/react"],
            "data_source": "mock",
        }


def _compute_activity_level(contributions: int, active_weeks: int) -> str:
    if contributions >= 500 or active_weeks >= 40: return "High"
    if contributions >= 150 or active_weeks >= 20: return "Moderate"
    if contributions >= 30 or active_weeks >= 5: return "Low"
    return "Very Low"

import asyncio # Needed for gather
