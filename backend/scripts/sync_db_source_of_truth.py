import os
import sys
import time
from sqlalchemy import text, inspect

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal
from app import models

def sync_database():
    print("=== FIXLY ERP: DATABASE SOURCE OF TRUTH SYNCHRONIZATION ===")
    
    # 1. Add is_leadership column to teams table if not present
    inspector = inspect(engine)
    existing_team_cols = [c["name"] for c in inspector.get_columns("teams")] if inspector.has_table("teams") else []
    
    with engine.connect() as conn:
        if "is_leadership" not in existing_team_cols:
            try:
                # PostgreSQL
                conn.execute(text("ALTER TABLE teams ADD COLUMN IF NOT EXISTS is_leadership BOOLEAN DEFAULT FALSE;"))
                conn.commit()
                print("[MIGRATION] Added 'is_leadership' column to 'teams' table.")
            except Exception as pg_err:
                try:
                    # SQLite fallback
                    conn.execute(text("ALTER TABLE teams ADD COLUMN is_leadership BOOLEAN DEFAULT 0;"))
                    conn.commit()
                    print("[MIGRATION SQLite] Added 'is_leadership' column to 'teams' table.")
                except Exception as sq_err:
                    print(f"[MIGRATION NOTICE] Column check: {sq_err}")

    db = SessionLocal()
    now_ms = int(time.time() * 1000)

    try:
        # 2. Canonical Teams Setup
        canonical_teams = [
            # Intern / Engineering Teams (is_leadership=False)
            {
                "name": "Mobile Application Development Team",
                "description": "Mobile & Web Frontend Application Engineering",
                "is_leadership": False
            },
            {
                "name": "DevOps Team",
                "description": "Cloud Infrastructure, CI/CD Pipelines & Site Reliability",
                "is_leadership": False
            },
            # Leadership Teams (is_leadership=True - visible and editable only by leadership)
            {
                "name": "Executive",
                "description": "Executive Leadership & Office of the CEO",
                "is_leadership": True
            },
            {
                "name": "Technology",
                "description": "Technology Strategy, Architecture & Engineering Direction",
                "is_leadership": True
            },
            {
                "name": "Career Development",
                "description": "Career Development Center (CDC) & Student Training",
                "is_leadership": True
            },
            {
                "name": "Academic Leadership",
                "description": "Academic Guidance, Mentorship & Curriculum Oversight",
                "is_leadership": True
            },
            {
                "name": "Operations",
                "description": "Company Operations, Facilities & Organizational Execution",
                "is_leadership": True
            },
            {
                "name": "Finance",
                "description": "Financial Planning, Resource Allocation & Accounting",
                "is_leadership": True
            },
            {
                "name": "Marketing",
                "description": "Brand Strategy, Outreach & Communications",
                "is_leadership": True
            }
        ]

        for t_info in canonical_teams:
            existing_t = db.query(models.Team).filter(models.Team.name.ilike(t_info["name"])).first()
            if not existing_t:
                new_t = models.Team(
                    name=t_info["name"],
                    description=t_info["description"],
                    is_leadership=t_info["is_leadership"],
                    createdAt=now_ms
                )
                db.add(new_t)
                print(f"[TEAM CREATED] '{t_info['name']}' (Leadership: {t_info['is_leadership']})")
            else:
                # Update is_leadership flag
                existing_t.is_leadership = t_info["is_leadership"]
                if t_info["description"] and not existing_t.description:
                    existing_t.description = t_info["description"]
                print(f"[TEAM UPDATED] '{existing_t.name}' (Leadership: {existing_t.is_leadership})")

        db.commit()

        # 3. Synchronize user team references to exact canonical team names
        team_mapping = {
            "Mobile Application Development": "Mobile Application Development Team",
            "mobile application development": "Mobile Application Development Team",
            "DevOps": "DevOps Team",
            "devops": "DevOps Team"
        }

        users = db.query(models.User).all()
        updated_users = 0
        for u in users:
            if u.team in team_mapping:
                old_team = u.team
                u.team = team_mapping[u.team]
                print(f"[USER TEAM SYNC] User '{u.name}' team updated from '{old_team}' -> '{u.team}'")
                updated_users += 1
            
            # 4. Synchronize user credentials in DB
            admin_pwd = os.getenv("ADMIN_PASSWORD", "AFixly@2026")
            viewer_pwd = os.getenv("VIEWER_PASSWORD", "VFixly@2026")
            default_pwd = os.getenv("DEFAULT_USER_PASSWORD", "Fixly@2026")

            if (u.role or "").lower() == "admin" and not u.password:
                u.password = admin_pwd
                print(f"[USER PWD] Set password for Admin user '{u.name}' in database.")
            elif (u.role or "").lower() == "viewer" and not u.password:
                u.password = viewer_pwd
                print(f"[USER PWD] Set password for Viewer user '{u.name}' in database.")
            elif not u.password:
                u.password = default_pwd
                print(f"[USER PWD] Set default password for user '{u.name}' in database.")

        # Also ensure existing logs match the canonical team name
        logs = db.query(models.Log).all()
        updated_logs = 0
        for l in logs:
            if l.team in team_mapping:
                l.team = team_mapping[l.team]
                updated_logs += 1

        db.commit()
        print(f"[OK] Completed synchronization. {updated_users} users and {updated_logs} logs updated.")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Synchronization failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    sync_database()
