import os
import sys
import unittest
from starlette.testclient import TestClient

os.environ["PYTHONIOENCODING"] = "utf-8"

from app.main import app
from app.database import SessionLocal
from app import models, seed_data

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("RUNNING ADMIN USER & TEAM CRUD TEST SUITE")
    print("=" * 60)

    # 1. USER CRUD TESTS
    print("\n--- 1. Testing User CRUD Endpoints ---")
    
    # A. Create a new user
    user_payload = {
        "name": "Test Engineer",
        "email": "test.engineer@fixly.internal",
        "rollNumber": "TEST-ENG-01",
        "team": "Engineering",
        "role": "backend_developer",
        "positionTitle": "Staff Backend Engineer",
        "accountStatus": "ACTIVE",
        "password": "TestPassword@123"
    }
    
    res = client.post("/api/users/", json=user_payload)
    assert res.status_code == 200, f"Failed to create user: {res.text}"
    created_user = res.json()
    user_id = created_user["id"]
    assert created_user["name"] == "Test Engineer"
    assert created_user["email"] == "test.engineer@fixly.internal"
    assert created_user["rollNumber"] == "TEST-ENG-01"
    assert created_user["role"] == "backend_developer"
    assert created_user["positionTitle"] == "Staff Backend Engineer"
    print(f"  [PASS] Created user ID {user_id}: {created_user['name']}")

    # B. Prevent duplicate email
    dup_email_payload = {
        "name": "Another Person",
        "email": "test.engineer@fixly.internal",
        "rollNumber": "TEST-DIFF-02"
    }
    res = client.post("/api/users/", json=dup_email_payload)
    assert res.status_code == 400, f"Expected 400 for duplicate email, got: {res.status_code}"
    print("  [PASS] Duplicate email rejected with 400")

    # C. Prevent duplicate roll number
    dup_roll_payload = {
        "name": "Another Person",
        "email": "different.email@fixly.internal",
        "rollNumber": "TEST-ENG-01"
    }
    res = client.post("/api/users/", json=dup_roll_payload)
    assert res.status_code == 400, f"Expected 400 for duplicate roll number, got: {res.status_code}"
    print("  [PASS] Duplicate roll number rejected with 400")

    # D. Get user by ID
    res = client.get(f"/api/users/{user_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "Test Engineer"
    print("  [PASS] Retrieved user by ID successfully")

    # E. Update user details
    update_payload = {
        "name": "Test Lead Engineer",
        "email": "test.lead@fixly.internal",
        "rollNumber": "TEST-LEAD-01",
        "role": "scrum_head",
        "positionTitle": "Principal Scrum Lead",
        "team": "Engineering",
        "accountStatus": "ACTIVE"
    }
    res = client.put(f"/api/users/{user_id}", json=update_payload)
    assert res.status_code == 200, f"Failed to update user: {res.text}"
    updated = res.json()
    assert updated["name"] == "Test Lead Engineer"
    assert updated["email"] == "test.lead@fixly.internal"
    assert updated["rollNumber"] == "TEST-LEAD-01"
    assert updated["role"] == "scrum_head"
    assert updated["positionTitle"] == "Principal Scrum Lead"
    print("  [PASS] Updated user details successfully")

    # 2. TEAM CRUD TESTS
    print("\n--- 2. Testing Team CRUD Endpoints ---")

    # A. Get all teams and check memberCount
    res = client.get("/api/teams/")
    assert res.status_code == 200
    teams = res.json()
    assert isinstance(teams, list)
    assert len(teams) > 0
    assert "memberCount" in teams[0]
    print(f"  [PASS] Fetched {len(teams)} teams with memberCount property")

    # B. Create a new team
    team_payload = {
        "name": "AI Research & Innovation",
        "description": "R&D team building generative intelligence tools",
        "leadId": user_id,
        "leadName": "Test Lead Engineer"
    }
    res = client.post("/api/teams/", json=team_payload)
    assert res.status_code == 200, f"Failed to create team: {res.text}"
    created_team = res.json()
    team_id = created_team["id"]
    assert created_team["name"] == "AI Research & Innovation"
    assert created_team["description"] == "R&D team building generative intelligence tools"
    assert created_team["leadId"] == user_id
    print(f"  [PASS] Created team ID {team_id}: {created_team['name']}")

    # C. Prevent duplicate team name
    res = client.post("/api/teams/", json={"name": "AI Research & Innovation"})
    assert res.status_code == 400
    print("  [PASS] Duplicate team name rejected with 400")

    # D. Assign user to this team
    res = client.put(f"/api/users/{user_id}", json={"team": "AI Research & Innovation"})
    assert res.status_code == 200
    
    # Verify team member count increased
    res = client.get(f"/api/teams/{team_id}")
    assert res.status_code == 200
    team_detail = res.json()
    assert team_detail["memberCount"] == 1
    assert len(team_detail["members"]) == 1
    assert team_detail["members"][0]["id"] == user_id
    print("  [PASS] Team member assigned and dynamically counted")

    # E. Update team name and test cascade rename
    rename_payload = {
        "name": "Applied AI Core",
        "description": "Updated mission for Applied AI Core",
        "leadId": user_id
    }
    res = client.put(f"/api/teams/{team_id}", json=rename_payload)
    assert res.status_code == 200
    renamed_team = res.json()
    assert renamed_team["name"] == "Applied AI Core"
    assert renamed_team["description"] == "Updated mission for Applied AI Core"

    # Verify assigned user's team was automatically updated to "Applied AI Core"
    res = client.get(f"/api/users/{user_id}")
    assert res.status_code == 200
    assert res.json()["team"] == "Applied AI Core", f"User team not cascaded! Got: {res.json()['team']}"
    print("  [PASS] Team renamed and automatically cascaded to assigned users")

    # F. Delete team and test member unassignment
    res = client.delete(f"/api/teams/{team_id}")
    assert res.status_code == 200
    
    # User's team should now be unassigned ("")
    res = client.get(f"/api/users/{user_id}")
    assert res.status_code == 200
    assert res.json()["team"] == "", f"Expected empty team, got: {res.json()['team']}"
    print("  [PASS] Deleted team and verified members safely unassigned")

    # Clean up test user
    res = client.delete(f"/api/users/{user_id}")
    assert res.status_code == 200
    print("  [PASS] Deleted test user successfully")

    print("\n" + "=" * 60)
    print("ALL ADMIN USER & TEAM CRUD TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
