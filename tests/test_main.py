from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. Test Health Check
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# 2. Test Create Leave (Success)
def test_create_leave():
    payload = {"employee_id": 1, "reason": "Sick Leave", "days": 2}
    response = client.post("/leaves/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Request created"
    assert data["data"]["employee_id"] == 1

# 3. Test Create Leave (Duplicate Error)
def test_create_duplicate_leave():
    # Attempt to create the same employee ID again (1 was created in the test above)
    # Note: TestClient shares state within the same session unless we reset db
    # For simplicity in this small project, we just use a new ID
    payload = {"employee_id": 1, "reason": "Holiday", "days": 5}
    response = client.post("/leaves/", json=payload)
    assert response.status_code == 400

# 4. Test Get Leave (Success)
def test_get_leave():
    response = client.get("/leaves/1")
    assert response.status_code == 200
    assert response.json()["reason"] == "Sick Leave"

# 5. Test Get Leave (Not Found)
def test_get_leave_not_found():
    response = client.get("/leaves/999")
    assert response.status_code == 404