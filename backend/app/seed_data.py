import time
import os
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session
from . import models

def migrate_sqlite_columns(engine):
    """Safely adds missing columns to existing tables if they do not exist."""
    from sqlalchemy import inspect
    inspector = inspect(engine)
    with engine.connect() as conn:
        try:
            # 1. Check users columns
            if inspector.has_table("users"):
                existing_cols = [c["name"] for c in inspector.get_columns("users")]
                
                user_cols = [
                    ("email", "VARCHAR"),
                    ("position_title", "VARCHAR DEFAULT ''"),
                    ("account_status", "VARCHAR DEFAULT 'ACTIVE'"),
                    ("requested_role", "VARCHAR"),
                    ("google_id", "VARCHAR"),
                    ("avatar_url", "VARCHAR"),
                ]
                
                for col_name, col_def in user_cols:
                    if col_name not in existing_cols:
                        try:
                            conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}"))
                            conn.commit()
                            print(f"[MIGRATED] Column users.{col_name}")
                        except Exception as e:
                            print(f"[NOTICE] Migrating users.{col_name}: {e}")

            # 2. Check logs columns
            if inspector.has_table("logs"):
                existing_log_cols = [c["name"] for c in inspector.get_columns("logs")]
                log_cols = [
                    ("attendance_mode", "VARCHAR DEFAULT 'office'")
                ]
                for col_name, col_def in log_cols:
                    if col_name not in existing_log_cols:
                        try:
                            conn.execute(text(f"ALTER TABLE logs ADD COLUMN {col_name} {col_def}"))
                            conn.commit()
                            print(f"[MIGRATED] Column logs.{col_name}")
                        except Exception as e:
                            print(f"[NOTICE] Migrating logs.{col_name}: {e}")

            # 3. Check moms columns
            if inspector.has_table("moms"):
                existing_mom_cols = [c["name"] for c in inspector.get_columns("moms")]
                mom_cols = [
                    ("title", "VARCHAR DEFAULT ''"),
                    ("team", "VARCHAR DEFAULT 'General'")
                ]
                for col_name, col_def in mom_cols:
                    if col_name not in existing_mom_cols:
                        try:
                            conn.execute(text(f"ALTER TABLE moms ADD COLUMN {col_name} {col_def}"))
                            conn.commit()
                            print(f"[MIGRATED] Column moms.{col_name}")
                        except Exception as e:
                            print(f"[NOTICE] Migrating moms.{col_name}: {e}")

            # 4. Check teams columns
            if inspector.has_table("teams"):
                existing_team_cols = [c["name"] for c in inspector.get_columns("teams")]
                team_cols = [
                    ("description", "VARCHAR DEFAULT ''"),
                    ("lead_name", "VARCHAR DEFAULT ''"),
                    ("lead_id", "INTEGER"),
                    ("is_leadership", "BOOLEAN DEFAULT FALSE"),
                    ("created_at", "BIGINT")
                ]
                for col_name, col_def in team_cols:
                    if col_name not in existing_team_cols:
                        try:
                            conn.execute(text(f"ALTER TABLE teams ADD COLUMN {col_name} {col_def}"))
                            conn.commit()
                            print(f"[MIGRATED] Column teams.{col_name}")
                        except Exception as e:
                            print(f"[NOTICE] Migrating teams.{col_name}: {e}")

        except Exception as e:
            print(f"[ERROR] Migration check error: {e}")

def seed_scrum_data(db: Session):
    """Seeds initial leadership accounts if the database has no users or unseeded leadership."""
    # If users already exist in production, skip running seed to protect database state
    existing_user_count = db.query(models.User).count()
    if existing_user_count > 0:
        admin_exists = db.query(models.User).filter(models.User.role.in_(["admin", "ceo"])).first()
        if admin_exists:
            return  # Production DB already populated, skip completely

    default_password = os.getenv("DEFAULT_USER_PASSWORD")
    if not default_password:
        return

    predefined_users = [
        # CEO (Full Admin)
        {
            "name": os.getenv("CEO_NAME", "Chief Executive Officer"),
            "email": os.getenv("CEO_EMAIL"),
            "rollNumber": "CEO-01",
            "team": "Executive",
            "role": "ceo",
            "positionTitle": "Chief Executive Officer",
            "accountStatus": "ACTIVE",
            "password": default_password
        },
        # CTO (Full Admin)
        {
            "name": os.getenv("CTO_NAME", "Chief Technology Officer"),
            "email": os.getenv("CTO_EMAIL"),
            "rollNumber": "CTO-01",
            "team": "Technology",
            "role": "cto",
            "positionTitle": "Chief Technology Officer",
            "accountStatus": "ACTIVE",
            "password": default_password
        },
        # CDC (View-Only Reviewer)
        {
            "name": os.getenv("CDC_NAME", "CDC Head"),
            "email": os.getenv("CDC_EMAIL"),
            "rollNumber": "CDC-01",
            "team": "Career Development",
            "role": "cdc",
            "positionTitle": "CDC Head - Career Development Center",
            "accountStatus": "ACTIVE",
            "password": default_password
        },
        # Program Head / Mentor (View-Only Reviewer)
        {
            "name": os.getenv("MENTOR_NAME", "Program Head / Mentor"),
            "email": os.getenv("MENTOR_EMAIL"),
            "rollNumber": "PROG-HEAD",
            "team": "Academic Leadership",
            "role": "mentor",
            "positionTitle": "Program Head / Mentor",
            "accountStatus": "ACTIVE",
            "password": default_password
        },
        # COO
        {
            "name": os.getenv("COO_NAME", "Chief Operating Officer"),
            "email": os.getenv("COO_EMAIL"),
            "rollNumber": "COO-01",
            "team": "Operations",
            "role": "coo",
            "positionTitle": "Chief Operating Officer",
            "accountStatus": "ACTIVE",
            "password": default_password
        },
        # CFO
        {
            "name": os.getenv("CFO_NAME", "Chief Financial Officer"),
            "email": os.getenv("CFO_EMAIL"),
            "rollNumber": "CFO-01",
            "team": "Finance",
            "role": "cfo",
            "positionTitle": "Chief Financial Officer",
            "accountStatus": "ACTIVE",
            "password": default_password
        },
        # CMO
        {
            "name": os.getenv("CMO_NAME", "Chief Marketing Officer"),
            "email": os.getenv("CMO_EMAIL"),
            "rollNumber": "CMO-01",
            "team": "Marketing",
            "role": "cmo",
            "positionTitle": "Chief Marketing Officer",
            "accountStatus": "ACTIVE",
            "password": default_password
        },
        # Admin / Tech Consultant
        {
            "name": os.getenv("ADMIN_NAME", "System Administrator"),
            "email": os.getenv("ADMIN_EMAIL"),
            "rollNumber": "ADMIN-01",
            "team": "Technology",
            "role": "admin",
            "positionTitle": "System Administrator",
            "accountStatus": "ACTIVE",
            "password": default_password
        },
    ]

    now_ms = int(time.time() * 1000)
    seeded_count = 0
    for u in predefined_users:
        if not u["email"]:
            continue

        existing = db.query(models.User).filter(
            (models.User.email == u["email"]) | 
            (models.User.rollNumber == u["rollNumber"])
        ).first()
        if not existing:
            new_u = models.User(
                name=u["name"],
                email=u["email"],
                rollNumber=u["rollNumber"],
                team=u["team"],
                role=u["role"],
                positionTitle=u["positionTitle"],
                accountStatus=u["accountStatus"],
                requestedRole=u.get("requestedRole"),
                createdAt=now_ms,
                password=u["password"]
            )
            db.add(new_u)
            seeded_count += 1
        else:
            # Do NOT overwrite existing user role, email, or password!
            # Only backfill non-sensitive empty fields
            if not existing.positionTitle and u["positionTitle"]:
                existing.positionTitle = u["positionTitle"]
            if not existing.team and u["team"]:
                existing.team = u["team"]
    
    if seeded_count > 0:
        db.commit()
        print(f"[OK] Seeded {seeded_count} initial leadership accounts.")

