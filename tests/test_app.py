from fastapi.testclient import TestClient

from src.app import app, activities


def test_unregister_participant_removes_the_student_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert unregister_response.status_code == 200

    payload = unregister_response.json()
    assert payload["message"] == f"Removed {email} from {activity_name}"

    updated_activity = client.get("/activities").json()[activity_name]
    assert email not in updated_activity["participants"]

    # Restore the in-memory state for the next test run.
    activities[activity_name]["participants"] = [
        participant for participant in activities[activity_name]["participants"] if participant != email
    ]
