import pytest
import sys
import os

# Allow importing backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ---------------------------------------------------
# Test 1: Health check endpoint
# ---------------------------------------------------
def test_status_endpoint():
    """API status endpoint should return 200 and online status."""
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


# ---------------------------------------------------
# Test 2: Root returns JSON health check
# ---------------------------------------------------
def test_root_health_check():
    """Root path should return JSON with API name and version."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "MentorIQ API"
    assert data["status"] == "online"
    assert "version" in data


# ---------------------------------------------------
# Test 3: Analyze with missing username returns 422
# ---------------------------------------------------
def test_analyze_missing_username():
    """Calling /api/analyze without a username param returns 422."""
    response = client.get("/api/analyze")
    assert response.status_code == 422


# ---------------------------------------------------
# Test 4: Analyze with empty username returns 422
# ---------------------------------------------------
def test_analyze_empty_username():
    """Empty username string should fail validation."""
    response = client.get("/api/analyze?username=")
    assert response.status_code == 422


# ---------------------------------------------------
# Test 5: Analyze with a valid username returns required fields
# ---------------------------------------------------
def test_analyze_returns_required_fields():
    """A successful analysis must contain all required output fields."""
    response = client.get("/api/analyze?username=khanolkarsujal")
    assert response.status_code == 200
    data = response.json()

    required_fields = [
        "status", "username", "maturity_score",
        "profile_career_level", "code_quality_label",
        "project_job_readiness", "technologies_used",
        "strengths", "skill_gaps", "mentor_match",
        "insights", "subscores", "avatar_url",
    ]
    for field in required_fields:
        assert field in data, f"Missing required field: '{field}'"


# ---------------------------------------------------
# Test 6: Maturity score is within valid range
# ---------------------------------------------------
def test_maturity_score_range():
    """Maturity score must be a float between 0.0 and 10.0."""
    response = client.get("/api/analyze?username=khanolkarsujal")
    assert response.status_code == 200
    score = response.json().get("maturity_score", -1)
    assert isinstance(score, (int, float)), "maturity_score must be numeric"
    assert 0 <= score <= 10, f"maturity_score {score} is out of range [0, 10]"


# ---------------------------------------------------
# Test 7: Subscores all present and valid
# ---------------------------------------------------
def test_subscores_structure():
    """Subscores must have the 5 expected keys, each 0-100."""
    response = client.get("/api/analyze?username=khanolkarsujal")
    assert response.status_code == 200
    subscores = response.json().get("subscores", {})
    expected_keys = [
        "code_quality", "architecture",
        "engineering_practices", "project_depth", "problem_solving"
    ]
    for key in expected_keys:
        assert key in subscores, f"Missing subscore: {key}"
        assert 0 <= subscores[key] <= 100, f"Subscore {key} out of range"


# ---------------------------------------------------
# Test 8: API version check
# ---------------------------------------------------
def test_api_version():
    """Status endpoint should report v3.x."""
    response = client.get("/api/status")
    assert response.status_code == 200
    assert "v3" in response.json().get("api_v", "")
