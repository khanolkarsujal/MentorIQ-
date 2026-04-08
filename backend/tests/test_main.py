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
# Test 2: Root serves the frontend HTML
# ---------------------------------------------------
def test_root_returns_html():
    """Root path should serve the frontend index.html."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


# ---------------------------------------------------
# Test 3: Analyze with missing username returns 422
# ---------------------------------------------------
def test_analyze_missing_username():
    """Calling /api/analyze without a username param returns 422."""
    response = client.get("/api/analyze")
    assert response.status_code == 422


# ---------------------------------------------------
# Test 4: Analyze with short username returns 422
# ---------------------------------------------------
def test_analyze_short_username():
    """Username shorter than 1 char should be rejected."""
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
        "status", "username", "skill_level",
        "maturity_score", "top_languages",
        "strengths", "skill_gaps", "mentor_match", "insights"
    ]
    for field in required_fields:
        assert field in data, f"Missing required field: '{field}'"


# ---------------------------------------------------
# Test 6: Maturity score is within valid range
# ---------------------------------------------------
def test_maturity_score_range():
    """Maturity score must be an integer between 1 and 10."""
    response = client.get("/api/analyze?username=khanolkarsujal")
    assert response.status_code == 200
    score = response.json().get("maturity_score", -1)
    assert isinstance(score, int), "maturity_score must be an integer"
    assert 1 <= score <= 10, f"maturity_score {score} is out of range [1, 10]"
