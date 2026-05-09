import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset the in-memory activities state before each test."""
    original_activities = {
        name: {
            "description": data["description"],
            "schedule": data["schedule"],
            "max_participants": data["max_participants"],
            "participants": data["participants"].copy(),
        }
        for name, data in activities.items()
    }

    yield

    activities.clear()
    activities.update(original_activities)
