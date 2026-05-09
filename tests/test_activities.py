from src.app import activities


def test_get_activities_returns_all_activities(client, reset_activities):
    """Arrange: client ready, Act: request activity list, Assert: activities are returned."""
    response = client.get("/activities")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()


class TestSignupForActivity:
    def test_signup_new_student(self, client, reset_activities):
        """Arrange: client ready, Act: sign up a new student, Assert: signup succeeds."""
        response = client.post("/activities/Basketball Team/signup?email=new.student@mergington.edu")

        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert "new.student@mergington.edu" in activities["Basketball Team"]["participants"]

    def test_signup_duplicate_student(self, client, reset_activities):
        """Arrange: student already registered, Act: attempt duplicate signup, Assert: returns 400."""
        activities["Basketball Team"]["participants"].append("duplicate@mergington.edu")

        response = client.post("/activities/Basketball Team/signup?email=duplicate@mergington.edu")

        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity(self, client, reset_activities):
        """Arrange: client ready, Act: sign up for missing activity, Assert: returns 404."""
        response = client.post("/activities/Fake Club/signup?email=student@mergington.edu")

        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_empty_email(self, client, reset_activities):
        """Arrange: client ready, Act: sign up with empty email, Assert: returns 400."""
        response = client.post("/activities/Basketball Team/signup?email=")

        assert response.status_code == 400
        assert "Invalid email" in response.json()["detail"]


class TestUnregisterForActivity:
    def test_unregister_existing_student(self, client, reset_activities):
        """Arrange: existing enrollment, Act: unregister, Assert: participant removed."""
        activities["Chess Club"]["participants"].append("student@mergington.edu")

        response = client.delete("/activities/Chess Club/signup?email=student@mergington.edu")

        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert "student@mergington.edu" not in activities["Chess Club"]["participants"]

    def test_unregister_nonexistent_student(self, client, reset_activities):
        """Arrange: no enrollment, Act: unregister missing student, Assert: returns 404."""
        response = client.delete("/activities/Chess Club/signup?email=nothere@mergington.edu")

        assert response.status_code == 404
        assert "Student not found" in response.json()["detail"]

    def test_unregister_nonexistent_activity(self, client, reset_activities):
        """Arrange: client ready, Act: unregister from missing activity, Assert: returns 404."""
        response = client.delete("/activities/Fake Club/signup?email=student@mergington.edu")

        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
