import time
import os
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session
from . import models

def migrate_sqlite_columns(engine):
    """Safely adds missing columns to existing SQLite tables if they do not exist."""
    with engine.connect() as conn:
        try:
            # 1. Check users columns
            result = conn.execute(text("PRAGMA table_info(users)")).fetchall()
            existing_cols = [r[1] for r in result]
            
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
            result = conn.execute(text("PRAGMA table_info(logs)")).fetchall()
            existing_log_cols = [r[1] for r in result]
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
            result = conn.execute(text("PRAGMA table_info(moms)")).fetchall()
            existing_mom_cols = [r[1] for r in result]
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
            result = conn.execute(text("PRAGMA table_info(teams)")).fetchall()
            existing_team_cols = [r[1] for r in result]
            team_cols = [
                ("description", "VARCHAR DEFAULT ''"),
                ("lead_name", "VARCHAR DEFAULT ''"),
                ("lead_id", "INTEGER"),
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
    """Seeds initial leadership accounts if they don't already exist. No mock data."""
    now_ms = int(time.time() * 1000)

    # Only real leadership accounts with real email addresses
    predefined_users = [
        # CEO (Full Admin)
        {
            "name": "Abhijeet",
            "email": "abhijeetlg1@gmail.com",
            "rollNumber": "CEO-01",
            "team": "Executive",
            "role": "ceo",
            "positionTitle": "Chief Executive Officer",
            "accountStatus": "ACTIVE",
            "password": os.getenv("DEFAULT_USER_PASSWORD", "Fixly@2026")
        },
        # CTO (Full Admin)
        {
            "name": "Karthik",
            "email": "notmedha@gmail.com",
            "rollNumber": "CTO-01",
            "team": "Technology",
            "role": "cto",
            "positionTitle": "Chief Technology Officer",
            "accountStatus": "ACTIVE",
            "password": os.getenv("DEFAULT_USER_PASSWORD", "Fixly@2026")
        },
        # CDC (View-Only Reviewer)
        {
            "name": "CDC Head",
            "email": "head.cdc@hitam.org",
            "rollNumber": "CDC-01",
            "team": "Career Development",
            "role": "cdc",
            "positionTitle": "CDC Head - Career Development Center",
            "accountStatus": "ACTIVE",
            "password": os.getenv("DEFAULT_USER_PASSWORD", "Fixly@2026")
        },
        # Program Head / Mentor (View-Only Reviewer)
        {
            "name": "Rohit Sir",
            "email": "programhead.csm@hitam.org",
            "rollNumber": "PROG-HEAD",
            "team": "Academic Leadership",
            "role": "mentor",
            "positionTitle": "Program Head / Mentor",
            "accountStatus": "ACTIVE",
            "password": os.getenv("DEFAULT_USER_PASSWORD", "Fixly@2026")
        },
        # COO
        {
            "name": "Nishanth",
            "email": "nishanth.chillumula@gmail.com",
            "rollNumber": "COO-01",
            "team": "Operations",
            "role": "coo",
            "positionTitle": "Chief Operating Officer",
            "accountStatus": "ACTIVE",
            "password": os.getenv("DEFAULT_USER_PASSWORD", "Fixly@2026")
        },
        # CFO
        {
            "name": "Dhanya",
            "email": "mamididhanyasvi@gmail.com",
            "rollNumber": "CFO-01",
            "team": "Finance",
            "role": "cfo",
            "positionTitle": "Chief Financial Officer",
            "accountStatus": "ACTIVE",
            "password": os.getenv("DEFAULT_USER_PASSWORD", "Fixly@2026")
        },
        # CMO
        {
            "name": "Anju Vaishnavi",
            "email": "anjuvaishnavi10@gmail.com",
            "rollNumber": "CMO-01",
            "team": "Marketing",
            "role": "cmo",
            "positionTitle": "Chief Marketing Officer",
            "accountStatus": "ACTIVE",
            "password": os.getenv("DEFAULT_USER_PASSWORD", "Fixly@2026")
        },
        # Admin / Tech Consultant
        {
            "name": "Sai Abhineeth",
            "email": "saiabhineeth23@gmail.com",
            "rollNumber": "ADMIN-01",
            "team": "Technology",
            "role": "admin",
            "positionTitle": "Admin / Tech Consultant",
            "accountStatus": "ACTIVE",
            "password": os.getenv("DEFAULT_USER_PASSWORD", "Fixly@2026")
        },
    ]

    for u in predefined_users:
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
        else:
            # Update existing user role and email if needed
            existing.email = u["email"]
            existing.role = u["role"]
            existing.positionTitle = u["positionTitle"]
            existing.accountStatus = u["accountStatus"]
            if u.get("password"):
                existing.password = u["password"]
    
    db.commit()
    print("[OK] Leadership accounts seeded successfully!")
