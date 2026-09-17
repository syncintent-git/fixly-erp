import os
import sys
import unittest
from starlette.testclient import TestClient

# Ensure ASCII output for Windows console
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["ADMIN_PASSWORD"] = "Fixly@2026"
os.environ["VIEWER_PASSWORD"] = "View@2026"

from app.main import app
from app.database import get_db, SessionLocal
from app import models, seed_data

client = TestClient(app)

def test_suite():
    print("=" * 60)
    print("STARTING FULL ROLE AND FUNCTIONALITY VERIFICATION SUITE")
    print("=" * 60)

    db = SessionLocal()
    try:
        # Seed database
        seed_data.seed_scrum_data(db)
        print("[OK] Database seeded successfully.")
        # Create dummy users for roles not seeded by seed_data.py
        missing_roles = ["scrum_head", "frontend_developer", "backend_developer", "devops_developer", "viewer"]
        import time
        now_ms = int(time.time() * 1000)
        for idx, role in enumerate(missing_roles):
            existing = db.query(models.User).filter(models.User.email == f"test_{role}@example.com").first()
            if not existing:
                u = models.User(
                    name=f"Test {role}",
                    email=f"test_{role}@example.com",
                    rollNumber=f"TEST-{idx}-{int(time.time())}", # ensuring uniqueness
                    team="Test Team",
                    role=role,
                    positionTitle=f"Test {role} Title",
                    accountStatus="ACTIVE",
                    createdAt=now_ms,
                    password="TestPassword@123"
                )
                db.add(u)
            else:
                existing.password = "TestPassword@123"
        db.commit()
        print("[OK] Dummy users for test seeded successfully.")

        # Create a dummy sprint for tests
        s = models.Sprint(
            sprintId="SP-TEST",
            name="Test Sprint 07",
            startDate=now_ms,
            endDate=now_ms + 1000000,
            createdAt=now_ms,
            status="ACTIVE"
        )
        db.add(s)
        db.commit()
        print("[OK] Dummy sprint seeded successfully.")
    finally:
        db.close()

    # 1. VERIFY ALL ROLES CAN LOGIN & HAVE ACCURATE PERMISSIONS
    test_roles = [
        {"role": "ceo", "expected_admin": True, "expected_view_only": False, "expected_scrum": True, "expected_intern": False},
        {"role": "cto", "expected_admin": True, "expected_view_only": False, "expected_scrum": True, "expected_intern": False},
        {"role": "coo", "expected_admin": True, "expected_view_only": False, "expected_scrum": True, "expected_intern": False},
        {"role": "cfo", "expected_admin": True, "expected_view_only": True, "expected_scrum": False, "expected_intern": False},
        {"role": "cmo", "expected_admin": True, "expected_view_only": True, "expected_scrum": False, "expected_intern": False},
        {"role": "cdc", "expected_admin": True, "expected_view_only": True, "expected_scrum": False, "expected_intern": False},
        {"role": "mentor", "expected_admin": True, "expected_view_only": True, "expected_scrum": False, "expected_intern": False},
        {"role": "scrum_head", "expected_admin": False, "expected_view_only": False, "expected_scrum": True, "expected_intern": False},
        {"role": "frontend_developer", "expected_admin": False, "expected_view_only": False, "expected_scrum": False, "expected_intern": True},
        {"role": "backend_developer", "expected_admin": False, "expected_view_only": False, "expected_scrum": False, "expected_intern": True},
        {"role": "devops_developer", "expected_admin": False, "expected_view_only": False, "expected_scrum": False, "expected_intern": True},
        {"role": "admin", "expected_admin": True, "expected_view_only": False, "expected_scrum": True, "expected_intern": False},
        {"role": "viewer", "expected_admin": True, "expected_view_only": True, "expected_scrum": False, "expected_intern": False},
    ]

    print("\n--- 1. Testing Demo Logins & Role Permissions ---")
    users_by_role = {}
    for r in test_roles:
        res = client.post("/api/auth/demo", json={"role": r["role"]})
        assert res.status_code == 200, f"Failed demo login for role {r['role']}: {res.text}"
        data = res.json()
        user = data["user"]
        perms = data["permissions"]
        users_by_role[r["role"]] = user

        assert perms["canAccessAdmin"] == r["expected_admin"], f"Role {r['role']} canAccessAdmin expected {r['expected_admin']}, got {perms['canAccessAdmin']}"
        assert perms["isViewOnly"] == r["expected_view_only"], f"Role {r['role']} isViewOnly expected {r['expected_view_only']}, got {perms['isViewOnly']}"
        assert perms["canManageScrum"] == r["expected_scrum"], f"Role {r['role']} canManageScrum expected {r['expected_scrum']}, got {perms['canManageScrum']}"
        assert perms["isIntern"] == r["expected_intern"], f"Role {r['role']} isIntern expected {r['expected_intern']}, got {perms['isIntern']}"
        print(f"  [PASS] Role '{r['role']}' authenticated: {user['name']} ({user['positionTitle']})")

    # 2. VERIFY ROLL NUMBER & PASSWORD LOGIN
    print("\n--- 2. Testing Roll Number & Password Login ---")
    res = client.post("/api/users/login", json={"rollNumber": "CEO-01", "password": "Fixly@2026"})
    assert res.status_code == 200, f"Roll login failed: {res.text}"
    print(f"  [PASS] CEO login via rollNumber: {res.json()['name']}")

    db = SessionLocal()
    try:
        frontend_intern = db.query(models.User).filter(models.User.email == "test_frontend_developer@example.com").first()
        intern_roll = frontend_intern.rollNumber
    finally:
        db.close()

    res = client.post("/api/users/login", json={"rollNumber": intern_roll, "password": "TestPassword@123"})
    assert res.status_code == 200, f"Intern login failed: {res.text}"
    print(f"  [PASS] Intern login via rollNumber: {res.json()['name']}")

    # 3. VERIFY ADMIN & VIEWER SPECIAL LOGINS
    print("\n--- 3. Testing Administrator & Viewer Console Logins ---")
    res = client.post("/api/users/admin-login", json={"username": "admin", "password": "Fixly@2026"})
    assert res.status_code == 200, f"Admin login failed: {res.text}"
    print(f"  [PASS] Admin console login: {res.json()['name']}")

    res = client.post("/api/users/admin-login", json={"username": "viewer", "password": "View@2026"})
    assert res.status_code == 200, f"Viewer console login failed: {res.text}"
    print(f"  [PASS] Viewer console login: {res.json()['name']}")

    # 4. VERIFY USERS LISTING
    print("\n--- 4. Testing User Directory Routes ---")
    for endpoint in ["/api/users", "/api/users/", "/api/users/all"]:
        res = client.get(endpoint)
        assert res.status_code == 200, f"Failed {endpoint}: {res.text}"
        assert len(res.json()) >= 10, f"Expected at least 10 users from {endpoint}"
        print(f"  [PASS] {endpoint} returned {len(res.json())} users")

    # 5. VERIFY SCRUM SPRINTS & ACTIVE SPRINT
    print("\n--- 5. Testing Scrum Sprints ---")
    res = client.get("/api/scrum/sprints/active")
    assert res.status_code == 200, f"Failed active sprint: {res.text}"
    active_sprint = res.json()
    assert active_sprint is not None, "No active sprint returned"
    print(f"  [PASS] Active Sprint found: {active_sprint['name']} (Status: {active_sprint['status']})")

    res = client.get("/api/scrum/sprints")
    assert res.status_code == 200, f"Failed list sprints: {res.text}"
    sprints = res.json()
    assert len(sprints) > 0, "Sprint list is empty"
    print(f"  [PASS] Sprints list returned {len(sprints)} sprints")

    # 6. VERIFY STORIES & TASKS LIFECYCLE
    print("\n--- 6. Testing Story & Task Creation & Review Workflow ---")
    scrum_head = users_by_role["scrum_head"]
    alex_intern = users_by_role["frontend_developer"]
    mentor = users_by_role["mentor"]

    # Create a user story
    story_payload = {
        "sprintId": active_sprint["id"],
        "title": "Automated Test Story for Role Audit",
        "description": "Verifying story creation and task lifecycle",
        "priority": "HIGH",
        "assignedToId": alex_intern["id"],
        "dueDate": "2026-09-30"
    }
    res = client.post(f"/api/scrum/stories?user_id={scrum_head['id']}", json=story_payload)
    assert res.status_code == 200, f"Failed story creation: {res.text}"
    created_story = res.json()
    print(f"  [PASS] Story created: {created_story['storyId']} - {created_story['title']}")

    # Create a task under this story
    task_payload = {
        "storyId": created_story["id"],
        "title": "Automated Test Task Implementation",
        "description": "Build automated test verification component",
        "assignedToId": alex_intern["id"]
    }
    res = client.post(f"/api/scrum/tasks?user_id={scrum_head['id']}", json=task_payload)
    assert res.status_code == 200, f"Failed task creation: {res.text}"
    created_task = res.json()
    print(f"  [PASS] Task created: {created_task['taskId']} - {created_task['title']}")

    # Intern advances status to IN_PROGRESS
    res = client.put(f"/api/scrum/tasks/{created_task['id']}/status?user_id={alex_intern['id']}", json={"status": "IN_PROGRESS"})
    assert res.status_code == 200, f"Failed task status update: {res.text}"
    print(f"  [PASS] Task status updated to IN_PROGRESS")

    # Intern submits work for review (PENDING_APPROVAL)
    submit_payload = {
        "submissionNotes": "PR created and unit tests pass with 100% coverage.",
        "submissionLink": "https://github.com/fixly-erp/project-tracker/pull/42"
    }
    res = client.post(f"/api/scrum/tasks/{created_task['id']}/submit?user_id={alex_intern['id']}", json=submit_payload)
    assert res.status_code == 200, f"Failed task submission: {res.text}"
    submitted_task = res.json()
    assert submitted_task["status"] == "PENDING_APPROVAL", f"Expected PENDING_APPROVAL, got {submitted_task['status']}"
    print(f"  [PASS] Task submitted for approval (Status: {submitted_task['status']})")

    # TEST ROLE SECURITY: View-only reviewer (Mentor) tries to approve task (MUST BE BLOCKED WITH 403)
    res = client.post(f"/api/scrum/tasks/{created_task['id']}/review?reviewer_id={mentor['id']}", json={"decision": "APPROVED", "feedback": "Looks good"})
    assert res.status_code == 403, f"Security violation: View-only reviewer was able to review task! Status: {res.status_code}"
    print(f"  [PASS] Role Security Enforced: View-only reviewer (Mentor) blocked with 403")

    # TEST ROLE SECURITY: Intern tries to approve task (MUST BE BLOCKED WITH 403)
    res = client.post(f"/api/scrum/tasks/{created_task['id']}/review?reviewer_id={alex_intern['id']}", json={"decision": "APPROVED", "feedback": "Self-approval"})
    assert res.status_code == 403, f"Security violation: Intern was able to approve task! Status: {res.status_code}"
    print(f"  [PASS] Role Security Enforced: Intern blocked from approving task with 403")

    # Authorized Scrum Head approves task
    res = client.post(f"/api/scrum/tasks/{created_task['id']}/review?reviewer_id={scrum_head['id']}", json={"decision": "APPROVED", "feedback": "Excellent quality, fully verified."})
    assert res.status_code == 200, f"Authorized review failed: {res.text}"
    approved_task = res.json()
    assert approved_task["status"] == "APPROVED", f"Expected APPROVED, got {approved_task['status']}"
    print(f"  [PASS] Authorized Scrum Head successfully approved task (Status: {approved_task['status']})")

    # Clean up test story & task
    res = client.delete(f"/api/scrum/stories/{created_story['id']}")
    assert res.status_code == 200, f"Failed story deletion: {res.text}"
    print(f"  [PASS] Test story and tasks cleaned up")

    # 7. VERIFY PENDING USER REGISTRATION & APPROVAL
    print("\n--- 7. Testing User Registration & Approval Pipeline ---")
    res = client.get("/api/scrum/pending-users")
    assert res.status_code == 200, f"Failed get pending users: {res.text}"
    pending_users = res.json()
    print(f"  [PASS] Fetched {len(pending_users)} pending users")

    # Register a new test applicant
    new_user_payload = {
        "name": "Audit Test Applicant",
        "email": "audit.applicant@fixly.internal",
        "requestedRole": "frontend_developer"
    }
    res = client.post("/api/auth/onboard-role", json=new_user_payload)
    assert res.status_code == 200, f"Failed onboarding applicant: {res.text}"
    onboarded = res.json()
    applicant_id = onboarded["user"]["id"]
    print(f"  [PASS] Registered test applicant ID: {applicant_id}")

    # Approve applicant by CEO
    ceo = users_by_role["ceo"]
    approve_payload = {
        "role": "frontend_developer",
        "team": "Frontend",
        "positionTitle": "Frontend Developer Intern"
    }
    res = client.post(f"/api/scrum/users/{applicant_id}/approve?reviewer_id={ceo['id']}", json=approve_payload)
    assert res.status_code == 200, f"Failed approving user: {res.text}"
    assert res.json()["accountStatus"] == "ACTIVE", f"Expected ACTIVE, got {res.json()['accountStatus']}"
    print(f"  [PASS] Applicant approved and activated by CEO")

    # Clean up test applicant
    res = client.delete(f"/api/users/{applicant_id}")
    assert res.status_code == 200, f"Failed to delete test applicant: {res.text}"
    print(f"  [PASS] Test applicant cleaned up")

    # 8. VERIFY MINUTES OF MEETING (MoM)
    print("\n--- 8. Testing Minutes of Meeting (MoM) Endpoints ---")
    for endpoint in ["/api/mom/all", "/api/moms/all", "/api/mom", "/api/moms"]:
        res = client.get(endpoint)
        assert res.status_code == 200, f"Failed {endpoint}: {res.text}"
        print(f"  [PASS] {endpoint} returned {len(res.json())} MoM records")

    # Create a test MoM
    mom_payload = {
        "title": "Audit Test Meeting",
        "team": "Engineering",
        "date": "2026-09-13",
        "agenda": "Verify ERP MoM flow",
        "attendees": "Alex, Priya, Rahul",
        "content": "<p>Test MoM content verified.</p>",
        "created_by": "Alex Carter"
    }
    res = client.post("/api/mom/text", json=mom_payload)
    assert res.status_code == 200, f"Failed to create MoM: {res.text}"
    created_mom = res.json()
    assert created_mom["title"] == "Audit Test Meeting"
    print(f"  [PASS] MoM created: {created_mom['id']} - {created_mom['title']}")

    # Clean up test MoM
    res = client.delete(f"/api/moms/delete/{created_mom['id']}")
    assert res.status_code == 200, f"Failed to delete MoM: {res.text}"
    print(f"  [PASS] Test MoM deleted successfully")

    # 9. VERIFY DAILY LOGS & ATTENDANCE
    print("\n--- 9. Testing Daily Work Logs & Attendance ---")
    for endpoint in ["/api/logs/all", "/api/logs"]:
        res = client.get(endpoint)
        assert res.status_code == 200, f"Failed {endpoint}: {res.text}"
        print(f"  [PASS] {endpoint} returned {len(res.json())} daily log records")

    log_payload = {
        "date": "2026-09-13",
        "workDone": "Implemented automated role and functionality test suite",
        "nextDayGoal": "Run end-to-end frontend production validation",
        "attendanceMode": "office",
        "name": "Alex Carter",
        "rollNumber": "FX-1001",
        "team": "Frontend",
        "user_id": alex_intern["id"]
    }
    res = client.post("/api/logs/submit", json=log_payload)
    assert res.status_code == 200, f"Failed submitting log: {res.text}"
    created_log = res.json()
    assert created_log["workDone"] == log_payload["workDone"]
    print(f"  [PASS] Daily log created: Log ID {created_log['id']}")

    # Update log
    res = client.put(f"/api/logs/update/{created_log['id']}", json={"workDone": "Updated work done for test verification"})
    assert res.status_code == 200, f"Failed updating log: {res.text}"
    print(f"  [PASS] Daily log updated successfully")

    # 10. VERIFY COMPANY CALENDAR & HOLIDAYS
    print("\n--- 10. Testing Company Calendar & Holidays ---")
    res = client.get("/api/holidays/all")
    assert res.status_code == 200, f"Failed holidays list: {res.text}"
    print(f"  [PASS] /api/holidays/all returned {len(res.json())} holidays")

    holiday_payload = {
        "name": "Audit Foundation Day",
        "date": "2026-10-01"
    }
    res = client.post("/api/holidays/create", json=holiday_payload)
    assert res.status_code == 200, f"Failed creating holiday: {res.text}"
    created_h = res.json()
    print(f"  [PASS] Created holiday: {created_h['id']} - {created_h['name']}")

    res = client.delete(f"/api/holidays/delete/{created_h['id']}")
    assert res.status_code == 200, f"Failed deleting holiday: {res.text}"
    print(f"  [PASS] Deleted holiday successfully")

    # 11. VERIFY AUDIT TRAIL LOGS
    print("\n--- 11. Testing Audit Trail Logs ---")
    res = client.get("/api/scrum/audit-logs")
    assert res.status_code == 200, f"Failed audit trail: {res.text}"
    audit_logs = res.json()
    assert len(audit_logs) > 0, "Audit logs list is empty"
    first_log = audit_logs[0]
    assert "createdAt" in first_log, "Missing createdAt in audit log"
    assert "actorName" in first_log, "Missing actorName in audit log"
    print(f"  [PASS] Audit logs returned {len(audit_logs)} events (latest: [{first_log['actorName']}] {first_log['action']} {first_log['details']})")

    print("\n" + "=" * 60)
    print("ALL 11 VERIFICATION STAGES PASSED WITH ZERO ERRORS!")
    print("=" * 60)

if __name__ == "__main__":
    test_suite()
