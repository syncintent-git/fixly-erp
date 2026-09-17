import os
import requests
from starlette.testclient import TestClient
from app.main import app

class ClientAdapter:
    def __init__(self):
        try:
            r = requests.get("http://127.0.0.1:8000/", timeout=0.5)
            self.live = True
            print("[INFO] Running tests against live uvicorn server (http://127.0.0.1:8000)")
        except Exception:
            self.live = False
            self.client = TestClient(app)
            print("[INFO] Running tests in-process using Starlette TestClient")

    def get(self, url, **kwargs):
        if self.live:
            return requests.get(url, **kwargs)
        path = url.replace("http://127.0.0.1:8000", "")
        return self.client.get(path, **kwargs)

    def post(self, url, **kwargs):
        if self.live:
            return requests.post(url, **kwargs)
        path = url.replace("http://127.0.0.1:8000", "")
        return self.client.post(path, **kwargs)

    def put(self, url, **kwargs):
        if self.live:
            return requests.put(url, **kwargs)
        path = url.replace("http://127.0.0.1:8000", "")
        return self.client.put(path, **kwargs)

    def delete(self, url, **kwargs):
        if self.live:
            return requests.delete(url, **kwargs)
        path = url.replace("http://127.0.0.1:8000", "")
        return self.client.delete(path, **kwargs)

http_client = ClientAdapter()
BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("--- 1. Testing Health Check ---")
    res = http_client.get(f"{BASE_URL}/")
    assert res.status_code == 200
    print("[OK] Health check passed:", res.json())

    print("\n--- 2. Testing Predefined Leadership Auth ---")
    # CEO
    res = http_client.post(f"{BASE_URL}/api/auth/demo", json={"role": "ceo"})
    assert res.status_code == 200
    ceo_data = res.json()
    assert ceo_data["permissions"]["canAccessAdmin"] is True
    assert ceo_data["permissions"]["isViewOnly"] is False
    print("[OK] CEO Auth:", ceo_data["user"]["email"], ceo_data["permissions"])

    # CDC (View-Only Reviewer)
    res = http_client.post(f"{BASE_URL}/api/auth/demo", json={"role": "cdc"})
    assert res.status_code == 200
    cdc_data = res.json()
    assert cdc_data["permissions"]["canAccessAdmin"] is True
    assert cdc_data["permissions"]["isViewOnly"] is True
    print("[OK] CDC Auth (View-Only):", cdc_data["user"]["email"], cdc_data["permissions"])

    # Program Head / Mentor (View-Only Reviewer)
    res = http_client.post(f"{BASE_URL}/api/auth/demo", json={"role": "mentor"})
    assert res.status_code == 200
    prog_data = res.json()
    assert prog_data["permissions"]["canAccessAdmin"] is True
    assert prog_data["permissions"]["isViewOnly"] is True
    print("[OK] Program Head Auth (View-Only):", prog_data["user"]["email"], prog_data["permissions"])

    # Intern: Frontend Developer
    res = http_client.post(f"{BASE_URL}/api/auth/demo", json={"role": "frontend_developer"})
    assert res.status_code == 200
    intern_data = res.json()
    assert intern_data["permissions"]["isIntern"] is True
    assert intern_data["permissions"]["canAccessAdmin"] is False
    print("[OK] Intern Auth:", intern_data["user"]["email"], intern_data["permissions"])

    print("\n--- 3. Testing Google Onboarding & Pending Approval Flow ---")
    import uuid, time
    applicant_email = f"test.applicant.{int(time.time())}.{uuid.uuid4().hex[:6]}@gmail.com"
    res = http_client.post(f"{BASE_URL}/api/auth/google", json={"email": applicant_email, "name": "Test Applicant"})
    assert res.status_code == 200
    assert res.json()["status"] == "ONBOARDING_REQUIRED"
    print("[OK] New user detected ONBOARDING_REQUIRED")

    # Select track: backend_developer
    res = http_client.post(f"{BASE_URL}/api/auth/onboard-role", json={
        "name": "Test Applicant",
        "email": applicant_email,
        "requestedRole": "backend_developer"
    })
    assert res.status_code == 200
    assert res.json()["status"] == "PENDING_APPROVAL"
    new_user_id = res.json()["user"]["id"]
    print(f"[OK] Onboarded user in PENDING_APPROVAL (ID: {new_user_id})")

    # Admin approves user
    res = http_client.post(f"{BASE_URL}/api/scrum/users/{new_user_id}/approve", json={
        "role": "backend_developer",
        "team": "Backend",
        "positionTitle": "Backend Developer Intern"
    }, params={"reviewer_id": ceo_data["user"]["id"]})
    assert res.status_code == 200
    assert res.json()["accountStatus"] == "ACTIVE"
    print("[OK] Admin approved user successfully, status is now ACTIVE!")

    print("\n--- 4. Testing Sprint Retrieval & 14-Day Cycle ---")
    res = http_client.get(f"{BASE_URL}/api/scrum/sprints")
    assert res.status_code == 200
    sprints = res.json()
    assert len(sprints) > 0
    sprint_07 = sprints[0]
    assert sprint_07["durationDays"] == 14
    print(f"[OK] Sprint retrieved: {sprint_07['name']} | Duration: {sprint_07['durationDays']} days | Progress: {sprint_07['progressPercentage']}%")

    print("\n--- 5. Testing Story & Task Creation ---")
    # Create story
    res = http_client.post(f"{BASE_URL}/api/scrum/stories", json={
        "sprintId": sprint_07["id"],
        "title": "Automated Test Story",
        "description": "Story for automated test",
        "priority": "HIGH"
    })
    assert res.status_code == 200
    story = res.json()
    assert story["storyId"].startswith("ST-")
    print(f"[OK] Created story: {story['storyId']} - {story['title']}")

    # Create task under story
    res = http_client.post(f"{BASE_URL}/api/scrum/tasks", json={
        "storyId": story["id"],
        "title": "Automated Test Task",
        "description": "Task for automated test",
        "assignedToId": intern_data["user"]["id"]
    })
    assert res.status_code == 200
    task = res.json()
    assert task["taskId"].startswith("TASK-")
    assert task["status"] == "TODO"
    print(f"[OK] Created task: {task['taskId']} - {task['title']}")

    print("\n--- 6. Testing Task Pipeline: TODO -> IN_PROGRESS -> SUBMIT -> REJECT -> APPROVE ---")
    # Move to IN_PROGRESS
    res = http_client.put(f"{BASE_URL}/api/scrum/tasks/{task['id']}/status", json={"status": "IN_PROGRESS"})
    assert res.status_code == 200
    assert res.json()["status"] == "IN_PROGRESS"
    print("[OK] Task moved to IN_PROGRESS")

    # Submit for approval
    res = http_client.post(f"{BASE_URL}/api/scrum/tasks/{task['id']}/submit", json={
        "submissionNotes": "Finished core logic with unit test coverage.",
        "submissionLink": "https://github.com/example/pr/1"
    })
    assert res.status_code == 200
    assert res.json()["status"] == "PENDING_APPROVAL"
    print("[OK] Task submitted, status is now PENDING_APPROVAL")

    # Review with REJECT -> must return to IN_PROGRESS with feedback
    res = http_client.post(f"{BASE_URL}/api/scrum/tasks/{task['id']}/review", json={
        "decision": "REJECTED",
        "feedback": "Please add integration tests for edge cases."
    }, params={"reviewer_id": ceo_data["user"]["id"]})
    assert res.status_code == 200
    rejected_task = res.json()
    assert rejected_task["status"] == "IN_PROGRESS"
    assert "edge cases" in rejected_task["reviewNotes"]
    print("[OK] Task rejected: correctly reverted to IN_PROGRESS with feedback notes!")

    # Intern resubmits
    res = http_client.post(f"{BASE_URL}/api/scrum/tasks/{task['id']}/submit", json={
        "submissionNotes": "Edge cases tests added."
    })
    assert res.status_code == 200

    # Review with APPROVED -> marks APPROVED
    res = http_client.post(f"{BASE_URL}/api/scrum/tasks/{task['id']}/review", json={
        "decision": "APPROVED",
        "feedback": "All requirements verified. Approved."
    }, params={"reviewer_id": ceo_data["user"]["id"]})
    assert res.status_code == 200
    approved_task = res.json()
    assert approved_task["status"] == "APPROVED"
    print("[OK] Task approved: status is now APPROVED!")

    # Verify CDC cannot approve (View-Only permission test)
    res = http_client.post(f"{BASE_URL}/api/scrum/tasks/{task['id']}/review", json={
        "decision": "APPROVED",
        "feedback": "CDC attempt"
    }, params={"reviewer_id": cdc_data["user"]["id"]})
    assert res.status_code == 403
    print("[OK] CDC view-only protection verified: Reviewer accounts cannot approve/reject tasks (403 Forbidden).")

    print("\n--- 7. Testing Audit Trail & Notifications ---")
    res = http_client.get(f"{BASE_URL}/api/scrum/audit-logs")
    assert res.status_code == 200
    logs = res.json()
    assert len(logs) > 0
    print(f"[OK] Audit logs working: {len(logs)} events recorded")

    res = http_client.get(f"{BASE_URL}/api/scrum/notifications", params={"recipient_id": intern_data["user"]["id"]})
    assert res.status_code == 200
    notifs = res.json()
    print(f"[OK] Notifications working: {len(notifs)} notifications found for intern Alex")

    print("\n[SUCCESS] ALL BACKEND API TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
