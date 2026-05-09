import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Check that new activities are present
    assert "Basketball Team" in data
    assert "Art Club" in data
    assert "Debate Club" in data


def test_signup_success():
    """Test successful signup for an activity"""
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@test.com")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up newstudent@test.com for Chess Club" in data["message"]


def test_signup_duplicate():
    """Test duplicate signup prevention"""
    # First signup
    client.post("/activities/Programming%20Class/signup?email=duplicate@test.com")
    # Second signup should fail
    response = client.post("/activities/Programming%20Class/signup?email=duplicate@test.com")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]


def test_signup_invalid_activity():
    """Test signup for non-existent activity"""
    response = client.post("/activities/NonExistent/signup?email=test@test.com")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_root_redirect():
    """Test root endpoint redirects to static"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Redirect
    assert "/static/index.html" in response.headers["location"]